import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATE_SCRIPT = REPO_ROOT / "scripts" / "validate_skill.py"


class ValidateSkillTests(unittest.TestCase):
    def test_validate_skill_passes_from_repo_root(self):
        result = subprocess.run(
            [sys.executable, str(VALIDATE_SCRIPT)],
            cwd=str(REPO_ROOT),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr + result.stdout)


if __name__ == "__main__":
    unittest.main()
