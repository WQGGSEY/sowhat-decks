"""Safety properties: hostile files and shared temp folders."""

import os
import stat

import pytest
from deckreview.inspect import inspect_pptx
from deckreview.render import lo_profile_dir


def test_deck_that_unzips_too_large_is_refused(decks):
    with pytest.raises(ValueError, match="too large"):
        inspect_pptx(decks["clean"], max_unzipped=1000)


@pytest.mark.skipif(not hasattr(os, "getuid"), reason="POSIX only")
def test_libreoffice_profile_is_private_to_the_user(tmp_path):
    prof = lo_profile_dir(base=tmp_path)
    st = os.stat(prof)
    assert st.st_uid == os.getuid()
    assert stat.S_IMODE(st.st_mode) & 0o077 == 0


@pytest.mark.skipif(not hasattr(os, "getuid"), reason="POSIX only")
def test_planted_profile_symlink_is_not_used(tmp_path):
    target = tmp_path / "attacker"
    target.mkdir()
    planted = tmp_path / f"deck-review-lo-{os.getuid()}"
    planted.symlink_to(target)
    prof = lo_profile_dir(base=tmp_path)
    assert prof.resolve() != target.resolve()
