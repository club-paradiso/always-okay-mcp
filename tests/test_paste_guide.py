import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_paste_guide_up_to_date():
    r = subprocess.run([sys.executable, str(ROOT / "tools/build_paste_guide.py"), "--check"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout


def test_paste_guide_self_contained():
    text = (ROOT / "ALWAYS-OKAY.md").read_text(encoding="utf-8")
    for leftover in ("references/", "scripts/", "CLAUDE_SKILL_DIR"):
        assert leftover not in text
    assert text.count("- **P") == 32
