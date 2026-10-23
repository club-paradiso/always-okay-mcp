"""The Skill's data-derived references must match the data snapshot and cite nothing that is missing."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_skill_refs_current_and_resolved():
    r = subprocess.run([sys.executable, str(ROOT / "tools/build_skill_refs.py"), "--check"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
