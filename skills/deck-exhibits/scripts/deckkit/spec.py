"""Load and validate a deck spec.

The JSON Schema file (deck-spec.schema.json, copied next to this module by
tools/sync_lib.py) is the contract. This module implements the subset of JSON
Schema the contract uses, so validation needs only the standard library, then
adds checks a schema cannot express (series lengths, highlight names).
"""
from __future__ import annotations

import json
import math
import pathlib
import re
from typing import Any

from .numbers import is_excel_format, is_python_format

SCHEMA_PATH = pathlib.Path(__file__).with_name("deck-spec.schema.json")
_SCHEMA: dict | None = None


class SpecError(ValueError):
    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("invalid deck spec:\n  " + "\n  ".join(errors))


def schema() -> dict:
    global _SCHEMA
    if _SCHEMA is None:
        _SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return _SCHEMA


def _resolve(node: dict) -> dict:
    while "$ref" in node:
        ref = node["$ref"]
        if not ref.startswith("#/"):
            raise ValueError(f"unsupported $ref {ref}")
        node = schema()
        for part in ref[2:].split("/"):
            node = node[part]
    return node


_TYPES = {
    "string": lambda v: isinstance(v, str),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "array": lambda v: isinstance(v, list),
    "object": lambda v: isinstance(v, dict),
    "null": lambda v: v is None,
}


def _discriminator(branches: list[dict]) -> str | None:
    """Property that holds a distinct const in every branch (e.g. 'layout', 'type')."""
    keys = None
    for b in branches:
        consts = {k for k, p in b.get("properties", {}).items() if "const" in _resolve(p)}
        keys = consts if keys is None else keys & consts
    return sorted(keys)[0] if keys else None


def _check(value: Any, node: dict, path: str, errors: list[str]) -> None:
    node = _resolve(node)

    if "oneOf" in node:
        branches = [_resolve(b) for b in node["oneOf"]]
        key = _discriminator(branches)
        if key and isinstance(value, dict):
            options = {_resolve(b["properties"][key])["const"]: b for b in branches}
            if isinstance(value.get(key), str) and value[key] in options:
                _check(value, options[value[key]], path, errors)
            else:
                errors.append(f"{path}.{key}: {value.get(key)!r} is not one of {sorted(options)}")
            return
        results = []
        for b in branches:
            errs: list[str] = []
            _check(value, b, path, errs)
            results.append(errs)
        if not any(len(r) == 0 for r in results):  # report the branch of the right type
            errors.extend(min(results, key=lambda r: (any(": expected " in e for e in r), len(r))))
        return

    if "const" in node and value != node["const"]:
        errors.append(f"{path}: must be {node['const']!r}")
        return
    if "enum" in node and value not in node["enum"]:
        errors.append(f"{path}: {value!r} is not one of {node['enum']}")
        return
    if "type" in node:
        types = node["type"] if isinstance(node["type"], list) else [node["type"]]
        if not any(_TYPES[t](value) for t in types):
            errors.append(f"{path}: expected {' or '.join(types)}, got {type(value).__name__}")
            return

    if isinstance(value, str):
        if "minLength" in node and len(value) < node["minLength"]:
            errors.append(f"{path}: must not be empty" if node["minLength"] == 1 else f"{path}: too short")
        if "maxLength" in node and len(value) > node["maxLength"]:
            errors.append(f"{path}: {len(value)} characters, max {node['maxLength']}")
        if "pattern" in node and not re.search(node["pattern"], value):
            errors.append(f"{path}: {value!r} does not match {node['pattern']}")
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        if not math.isfinite(value):
            errors.append(f"{path}: must be a finite number, not {value}")
            return
        if "minimum" in node and value < node["minimum"]:
            errors.append(f"{path}: {value} is below {node['minimum']}")
        if "maximum" in node and value > node["maximum"]:
            errors.append(f"{path}: {value} is above {node['maximum']}")
    elif isinstance(value, list):
        if "minItems" in node and len(value) < node["minItems"]:
            errors.append(f"{path}: {len(value)} items, min {node['minItems']}")
        if "maxItems" in node and len(value) > node["maxItems"]:
            errors.append(f"{path}: {len(value)} items, max {node['maxItems']}")
        if "items" in node:
            for i, item in enumerate(value):
                _check(item, node["items"], f"{path}[{i}]", errors)
    elif isinstance(value, dict):
        props = node.get("properties", {})
        for key in node.get("required", []):
            if key not in value:
                errors.append(f"{path}.{key}: required")
        for key, item in value.items():
            if key in props:
                _check(item, props[key], f"{path}.{key}", errors)
            elif node.get("additionalProperties") is False:
                errors.append(f"{path}.{key}: unknown field (allowed: {', '.join(props)})")


def _semantic(spec: dict, errors: list[str]) -> None:
    for i, slide in enumerate(spec.get("slides", [])):
        if not isinstance(slide, dict):
            continue
        path = f"slides[{i}]"
        if slide.get("layout") == "appendix":
            given = [k for k in ("bullets", "table", "exhibit") if k in slide]
            if len(given) != 1:
                errors.append(f"{path}: appendix needs exactly one of bullets, table, exhibit (got {given or 'none'})")
        for key in ("table",):
            if isinstance(slide.get(key), dict):
                _check_table(slide[key], f"{path}.{key}", errors)
        ex = slide.get("exhibit")
        if isinstance(ex, dict):
            _check_exhibit(ex, f"{path}.exhibit", errors)


def _check_table(t: dict, path: str, errors: list[str]) -> None:
    fmt = t.get("number_format")
    if fmt and not (is_excel_format(fmt) or is_python_format(fmt)):
        errors.append(f"{path}.number_format: {fmt!r} is not a number format "
                      "(Excel style like '#,##0.0' or '0%', or Python style like ',.1f')")
    cols = t.get("columns", [])
    for r, row in enumerate(t.get("rows", [])):
        if isinstance(row, list) and len(row) != len(cols):
            errors.append(f"{path}.rows[{r}]: {len(row)} cells but {len(cols)} columns")
    hl = t.get("highlight") or {}
    for r in hl.get("rows", []):
        if r >= len(t.get("rows", [])):
            errors.append(f"{path}.highlight.rows: row {r} does not exist")
    for c in hl.get("cols", []):
        if c >= len(cols):
            errors.append(f"{path}.highlight.cols: column {c} does not exist")


def _check_exhibit(ex: dict, path: str, errors: list[str]) -> None:
    kind = ex.get("type")
    cats = ex.get("categories", [])
    if kind == "bar":
        if len(ex.get("values", [])) != len(cats):
            errors.append(f"{path}.values: {len(ex.get('values', []))} values but {len(cats)} categories")
        for h in ex.get("highlight", []):
            if isinstance(h, int) and not isinstance(h, bool):
                if not 0 <= h < len(cats):
                    errors.append(f"{path}.highlight: index {h} is outside the categories")
            elif h not in cats:
                errors.append(f"{path}.highlight: {h!r} is not a category")
    elif kind in ("line", "stacked_bar", "stacked_bar_100"):
        names = []
        for s, series in enumerate(ex.get("series", [])):
            if isinstance(series, dict):
                names.append(series.get("name"))
                if len(series.get("values", [])) != len(cats):
                    errors.append(f"{path}.series[{s}].values: {len(series.get('values', []))} values but {len(cats)} categories")
        if "highlight" in ex and ex["highlight"] not in names:
            errors.append(f"{path}.highlight: {ex['highlight']!r} is not a series name")
        if kind != "line":
            for s, series in enumerate(ex.get("series", [])):
                negative = [v for v in series.get("values", []) if v is not None and v < 0]
                if negative:
                    errors.append(f"{path}.series[{s}].values: stacked bars need values of 0 or more "
                                  f"(found {negative[0]}); show a change that goes up and down as a bar chart")
    elif kind == "highlight_table":
        _check_table(ex, path, errors)
    elif kind == "process":
        if ex.get("highlight", 0) >= len(ex.get("steps", [])):
            errors.append(f"{path}.highlight: step {ex['highlight']} does not exist")


def validate(spec: Any) -> list[str]:
    """All problems with the spec, as readable strings. Empty list = valid."""
    errors: list[str] = []
    _check(spec, schema(), "spec", errors)
    if not errors:  # cross-field checks assume the types are right, so they run on a schema-valid spec only
        _semantic(spec, errors)
    return [e.replace("spec.slides", "slides", 1) for e in errors]


def load(path: str | pathlib.Path) -> dict:
    """Read and validate a spec file. Raises SpecError listing every problem."""
    try:
        data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SpecError([f"{path}: not valid JSON ({exc})"]) from exc
    errors = validate(data)
    if errors:
        raise SpecError(errors)
    return data
