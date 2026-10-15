"""Unit tests for the demo application's HTML structure checker."""
from pathlib import Path
import tempfile
import unittest

from checks.check_html import main


class CheckHtmlTests(unittest.TestCase):
    def check_document(self, content):
        with tempfile.TemporaryDirectory() as directory:
            document = Path(directory) / "index.html"
            document.write_text(content, encoding="utf-8")
            return main(str(document))

    def test_accepts_a_well_formed_demo_document(self):
        result = self.check_document(
            "<!doctype html><html><head><title>Demo</title></head>"
            "<body><main>Application</main></body></html>"
        )
        self.assertEqual(result, 0)

    def test_rejects_mismatched_tags(self):
        result = self.check_document(
            "<!doctype html><html><head><title>Demo</title></head>"
            "<body><main>Application</body></main></html>"
        )
        self.assertEqual(result, 1)

    def test_rejects_missing_required_elements(self):
        result = self.check_document("<!doctype html><html><body></body></html>")
        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
