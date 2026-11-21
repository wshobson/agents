import io
import tempfile
import unittest
from pathlib import Path

from report.cli import main


class CliTextTest(unittest.TestCase):
    def run_cli(self, text, *extra):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "r.txt"
            path.write_text(text, encoding="utf-8")
            out = io.StringIO()
            code = main([str(path), *extra], out=out)
            return code, out.getvalue()

    def test_text_output_is_stable(self):
        # Downstream tooling parses this output byte for byte. Do not change it.
        code, text = self.run_cli("b=fail\na=pass\nc=fail\n")
        self.assertEqual(code, 1)
        self.assertEqual(text, "1/3 passed\nFAIL b\nFAIL c\n")

    def test_all_pass(self):
        code, text = self.run_cli("a=pass\n")
        self.assertEqual((code, text), (0, "1/1 passed\n"))


if __name__ == "__main__":
    unittest.main()
