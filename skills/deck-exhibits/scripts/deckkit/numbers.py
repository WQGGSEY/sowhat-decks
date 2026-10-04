"""Number formats: one rule for validation, chart labels and table cells (standard library only).

Charts take an Excel-style format, limited to a safe set PowerPoint and LibreOffice
both draw the same way: optional currency sign, "0" or "#,##0", up to 6 decimals,
optional "%". Tables take the same Excel style or a Python format spec (",.1f").
"""
from __future__ import annotations

import re

# keep in sync with $defs.ex_common.number_format.pattern in deck-spec.schema.json (a test checks it)
EXCEL_FORMAT = r"^[$€£¥₩]?(#,##0|0)(\.0{1,6})?%?$"
_EXCEL = re.compile(EXCEL_FORMAT)


def is_excel_format(fmt: str) -> bool:
    return bool(_EXCEL.match(fmt))


def is_python_format(fmt: str) -> bool:
    try:
        format(1234.5, fmt)
        format(1234, fmt)
    except (ValueError, TypeError):
        return False
    return True


def auto_format(values: list) -> str:
    """'#,##0' for whole numbers, '#,##0.0' otherwise."""
    nums = [v for v in values if isinstance(v, (int, float)) and not isinstance(v, bool)]
    return "#,##0" if all(float(v).is_integer() for v in nums) else "#,##0.0"


def fmt_number(v, excel_fmt: str) -> str:
    """Format a number the way the (safe) Excel format draws it in the chart."""
    if v is None:
        return "–"
    m = _EXCEL.match(excel_fmt)
    if not m:
        raise ValueError(f"unsupported number format {excel_fmt!r}")
    currency = excel_fmt[0] if excel_fmt[0] in "$€£¥₩" else ""
    decimals = len(m.group(2)) - 1 if m.group(2) else 0
    percent = excel_fmt.endswith("%")
    comma = "," if m.group(1) == "#,##0" else ""
    value = v * 100 if percent else v
    sign = "-" if value < 0 else ""
    return f"{sign}{currency}{abs(value):{comma}.{decimals}f}{'%' if percent else ''}"


def format_cell(v, fmt: str | None) -> str:
    """Table cell text: Excel-style or Python-style format for numbers, text as written."""
    if v is None:
        return "–"
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return str(v)
    if fmt:
        return fmt_number(v, fmt) if is_excel_format(fmt) else format(v, fmt)
    return f"{v:,}" if float(v).is_integer() else f"{v:,.1f}"
