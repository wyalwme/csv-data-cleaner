import subprocess
import sys
import unittest
from pathlib import Path

from main import clean_data


PROJECT_DIR = Path(__file__).parent
MAIN_FILE = PROJECT_DIR / "main.py"



class TestCleanData(unittest.TestCase):

    def test_missing_input_file(self):
        result = subprocess.run(
            [sys.executable, str(MAIN_FILE), "nonexistent.csv"],
            capture_output=True,
            text=True,
            cwd=PROJECT_DIR,
        )

        self.assertIn("Error: File not found: nonexistent.csv", result.stdout)
        self.assertEqual(result.returncode, 0)

    
    def test_unknown_argument(self):
        result = subprocess.run(
            [
                sys.executable,
                str(MAIN_FILE),
                "customers.csv",
                "--outpt",
                "result.csv",
            ],
            capture_output=True,
            text=True,
            cwd=PROJECT_DIR,
        )

        self.assertIn("Error: Unknown argument: --outpt", result.stdout)
        self.assertEqual(result.returncode, 0)

    
    def test_missing_output_filename(self):
        result = subprocess.run(
            [
                sys.executable,
                str(MAIN_FILE),
                "customers.csv",
                "--output",
            ],
            capture_output=True,
            text=True,
            cwd=PROJECT_DIR,
        )

        self.assertIn(
            "Error: Please specify an output filename.",
            result.stdout,
        )
        self.assertEqual(result.returncode, 0)

    
    def test_repeated_output_argument(self):
        result = subprocess.run(
            [
                sys.executable,
                str(MAIN_FILE),
                "customers.csv",
                "--output",
                "first.csv",
                "--output",
                "second.csv",
            ],
            capture_output=True,
            text=True,
            cwd=PROJECT_DIR,
        )

        self.assertIn(
            "Error: --output can only be used once.",
            result.stdout,
        )
        self.assertFalse((PROJECT_DIR / "first.csv").exists())
        self.assertFalse((PROJECT_DIR / "second.csv").exists())

    
    def test_unexpected_argument(self):
        result = subprocess.run(
            [
                sys.executable,
                str(MAIN_FILE),
                "customers.csv",
                "another.csv",
            ],
            capture_output=True,
            text=True,
            cwd=PROJECT_DIR,
        )

        self.assertIn(
            "Error: Unexpected argument: another.csv",
            result.stdout,
        )
        self.assertEqual(result.returncode, 0)

    
    def test_csv_without_headers(self):
        input_file = PROJECT_DIR / "test_no_headers.csv"

        try:
            input_file.write_text("", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(MAIN_FILE),
                    "test_no_headers.csv",
                ],
                capture_output=True,
                text=True,
                cwd=PROJECT_DIR,
            )

            self.assertIn(
                "Error: CSV headers are missing.",
                result.stdout,
            )
            self.assertEqual(result.returncode, 0)

        finally:
            input_file.unlink(missing_ok=True)

    
    def test_invalid_encoding(self):
        input_file = PROJECT_DIR / "test_invalid_encoding.csv"

        try:
            input_file.write_bytes(b"\xff\xfe\xfa")

            result = subprocess.run(
                [
                    sys.executable,
                    str(MAIN_FILE),
                    "test_invalid_encoding.csv",
                ],
                capture_output=True,
                text=True,
                cwd=PROJECT_DIR,
            )

            self.assertIn(
                "Error: Could not read CSV file:",
                result.stdout,
            )
            self.assertEqual(result.returncode, 0)

        finally:
            input_file.unlink(missing_ok=True)

    
    def test_absolute_input_and_output_paths(self):
        input_file = PROJECT_DIR / "test_absolute_input.csv"
        output_file = PROJECT_DIR / "test_absolute_output.csv"
        report_file = PROJECT_DIR / "test_absolute_output_report.txt"

        try:
            input_file.write_text(
                "name,email\nAlice,alice@example.com\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(MAIN_FILE),
                    str(input_file.resolve()),
                    "--output",
                    str(output_file.resolve()),
                ],
                capture_output=True,
                text=True,
                cwd=PROJECT_DIR,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output_file.exists())
            self.assertTrue(report_file.exists())

        finally:
            input_file.unlink(missing_ok=True)
            output_file.unlink(missing_ok=True)
            report_file.unlink(missing_ok=True)

    def test_custom_output_filename(self):
        output_file = PROJECT_DIR / "test_result.csv"
        report_file = PROJECT_DIR / "test_result_report.txt"

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(MAIN_FILE),
                    "customers.csv",
                    "--output",
                    "test_result.csv",
                ],
                capture_output=True,
                text=True,
                cwd=PROJECT_DIR,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output_file.exists())
            self.assertTrue(report_file.exists())
            self.assertIn("Cleaned file saved: test_result.csv", result.stdout)
            self.assertIn("Report saved: test_result_report.txt", result.stdout)

        finally:
            output_file.unlink(missing_ok=True)
            report_file.unlink(missing_ok=True)

    def test_removes_empty_rows(self):
        headers = ["name", "email"]
        rows = [
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "", "email": ""},
        ]

        cleaned, empty_count, duplicate_count = clean_data(headers, rows)

        self.assertEqual(len(cleaned), 1)
        self.assertEqual(empty_count, 1)
        self.assertEqual(duplicate_count, 0)

    def test_removes_duplicate_rows(self):
        headers = ["name", "email"]
        rows = [
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "Alice", "email": "alice@example.com"},
        ]

        cleaned, empty_count, duplicate_count = clean_data(headers, rows)

        self.assertEqual(len(cleaned), 1)
        self.assertEqual(empty_count, 0)
        self.assertEqual(duplicate_count, 1)

    def test_strips_whitespace(self):
        headers = ["name", "email"]
        rows = [
            {"name": "  Alice  ", "email": " alice@example.com "},
        ]

        cleaned, _, _ = clean_data(headers, rows)

        self.assertEqual(cleaned[0]["name"], "Alice")
        self.assertEqual(cleaned[0]["email"], "alice@example.com")

    
    def test_preserves_rows_with_missing_values(self):
        headers = ["name", "email"]
        rows = [
            {"name": "Alice", "email": ""},
            {"name": "Bob", "email": "bob@example.com"},
        ]

        cleaned, empty_count, duplicate_count = clean_data(headers, rows)

        self.assertEqual(len(cleaned), 2)
        self.assertEqual(cleaned[0]["email"], "")
        self.assertEqual(empty_count, 0)
        self.assertEqual(duplicate_count, 0)


if __name__ == "__main__":
    unittest.main()
