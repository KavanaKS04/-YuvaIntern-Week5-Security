import unittest
import tempfile
import sqlite3
from pathlib import Path
from unittest.mock import patch

import secure_student_app as app


class SecurityTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_students.db"

        self.db_patcher = patch.object(app, "DB_PATH", self.db_path)
        self.db_patcher.start()

        app.initialize_database()

    def tearDown(self):
        self.db_patcher.stop()
        self.temp_dir.cleanup()

    def test_valid_name(self):
        self.assertEqual(
            app.validate_name("Ananya Rao"),
            "Ananya Rao"
        )

    def test_invalid_name(self):
        with self.assertRaises(ValueError):
            app.validate_name("A")

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            app.validate_email("not-an-email")

    def test_marks_above_limit(self):
        with self.assertRaises(ValueError):
            app.validate_marks("150")

    def test_negative_marks(self):
        with self.assertRaises(ValueError):
            app.validate_marks("-10")

    def test_valid_marks(self):
        self.assertEqual(app.validate_marks("85"), 85.0)

    def test_duplicate_email_prevention(self):
        app.add_student("Ananya Rao", "ananya@example.com", 85)

        with self.assertRaises(sqlite3.IntegrityError):
            with app.database_connection() as connection:
                connection.execute(
                    "INSERT INTO students (name, email, marks) "
                    "VALUES (?, ?, ?)",
                    ("Another Student", "ananya@example.com", 90)
                )

    def test_sql_injection_input_rejected(self):
        malicious_name = "Robert'); DROP TABLE students;--"

        with self.assertRaises(ValueError):
            app.validate_name(malicious_name)

        # Confirm that the students table still exists.
        with app.database_connection() as connection:
            result = connection.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type = ? AND name = ?",
                ("table", "students")
            ).fetchone()

        self.assertIsNotNone(result)

    def test_database_table_exists(self):
        with app.database_connection() as connection:
            result = connection.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type = ? AND name = ?",
                ("table", "students")
            ).fetchone()

        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
