import io
import json
import tempfile
import unittest
from pathlib import Path

from report.cli import main


class CliJsonTest(unittest.TestCase):
    def run_cli(self, text, *extra):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "r.txt"
            path.write_text(text, encoding="utf-8")
            out = io.StringIO()
            code = main([str(path), *extra], out=out)
            return code, out.getvalue()

    def test_json(self):
        code, text = self.run_cli("c=fail\na=pass\nb=fail\n", "--json")
        self.assertEqual(code, 1)
        self.assertEqual(
            json.loads(text), {"total": 3, "passed": 1, "failed": 2, "failed_names": ["b", "c"]}
        )

    def test_text_still_stable(self):
        _, text = self.run_cli("b=fail\na=pass\nc=fail\n")
        self.assertEqual(text, "1/3 passed\nFAIL b\nFAIL c\n")


if __name__ == "__main__":
    unittest.main()
