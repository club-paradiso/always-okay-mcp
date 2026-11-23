"""The Skill's data-derived references must match the data snapshot and cite nothing that is missing."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_skill_refs_current_and_resolved():
    r = subprocess.run([sys.executable, str(ROOT / "tools/build_skill_refs.py"), "--check"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_skill_md_lists_every_move_and_taste_test():
    import json
    mv = json.loads((ROOT / "src/always_okay_mcp/data/moves.json").read_text(encoding="utf-8"))
    text = (ROOT / "plugins/always-okay/skills/always-okay/SKILL.md").read_text(encoding="utf-8")
    for item in mv["moves"] + mv["taste"]:
        assert f"- {item['id']} {item['name']} ({item['ko']})" in text, item["id"]
