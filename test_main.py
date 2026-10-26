
import unittest

from main import clean_data


class TestCleanData(unittest.TestCase):

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
