import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INIT_SCRIPT = REPO_ROOT / "scripts" / "init_research.py"
EXPECTED_HEADER = [
    "iteration",
    "metric_value",
    "delta",
    "delta_pct",
    "status",
    "description",
    "evaluator_source",
    "timestamp",
]


class InitResearchTests(unittest.TestCase):
    def test_scaffold_command_creates_expected_files_and_tsv_header(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "research-output"
            result = subprocess.run(
                [
                    sys.executable,
                    str(INIT_SCRIPT),
                    "--goal",
                    "Improve benchmark score",
                    "--metric",
                    "score",
                    "--direction",
                    "maximize",
                    "--output",
                    str(output_dir),
                ],
                cwd=str(REPO_ROOT),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr + result.stdout)
            self.assertTrue((output_dir / "research.md").is_file())
            self.assertTrue((output_dir / "research_log.md").is_file())
            results_path = output_dir / "autoresearch-results.tsv"
            self.assertTrue(results_path.is_file())

            header = results_path.read_text().splitlines()[0].split("\t")
            self.assertEqual(header, EXPECTED_HEADER)


if __name__ == "__main__":
    unittest.main()
