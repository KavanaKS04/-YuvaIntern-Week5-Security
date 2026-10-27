
import sqlite3
import re
from pathlib import Path
from contextlib import contextmanager

# Store the database in the project folder
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "students.db"


@contextmanager
def database_connection():
    """Open and safely close a database connection."""
    connection = sqlite3.connect(DB_PATH, timeout=10)

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        yield connection
        connection.commit()
    except sqlite3.Error:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database():
    """Create the student table if it does not exist."""
    with database_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                marks REAL NOT NULL CHECK(marks >= 0 AND marks <= 100)
            )
        """)


def validate_name(name):
    """Allow ordinary names containing letters and spaces."""
    name = name.strip()

    if not 2 <= len(name) <= 60:
        raise ValueError("Name must contain 2 to 60 characters.")

    if not all(character.isalpha() or character in " -'" for character in name):
        raise ValueError("Name contains invalid characters.")

    if not any(character.isalpha() for character in name):
        raise ValueError("Enter a valid name.")

    return name


def validate_email(email):
    """Perform basic email-format validation."""
    email = email.strip()

    if len(email) > 254:
        raise ValueError("Email address is too long.")

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.fullmatch(pattern, email):
        raise ValueError("Enter a valid email address.")

    return email


def validate_marks(marks):
    """Accept marks only in the range 0 to 100."""
    try:
        value = float(marks)
    except (TypeError, ValueError):
        raise ValueError("Marks must be a number.")

    if not 0 <= value <= 100:
        raise ValueError("Marks must be between 0 and 100.")

    return value


def add_student(name, email, marks):
    """Validate and insert a student using a parameterized query."""
    name = validate_name(name)
    email = validate_email(email)
    marks = validate_marks(marks)

    try:
        with database_connection() as connection:
            connection.execute(
                "INSERT INTO students (name, email, marks) VALUES (?, ?, ?)",
                (name, email, marks)
            )

        print("Student added successfully.")

    except sqlite3.IntegrityError:
        print("Could not add student. The email may already exist.")
    except sqlite3.Error:
        print("Database operation failed. Please try again.")


def view_students():
    """Display student records."""
    try:
        with database_connection() as connection:
            cursor = connection.execute(
                "SELECT student_id, name, email, marks "
                "FROM students ORDER BY student_id"
            )
            students = cursor.fetchall()

        if not students:
            print("No student records found.")
            return

        print("\n--- Student Records ---")
        for student in students:
            print(
                f"ID: {student[0]} | Name: {student[1]} | "
                f"Email: {student[2]} | Marks: {student[3]:.2f}"
            )

    except sqlite3.Error:
        print("Unable to retrieve student records.")


def search_student(email):
    """Search for a student using a parameterized query."""
    email = validate_email(email)

    try:
        with database_connection() as connection:
            student = connection.execute(
                "SELECT student_id, name, email, marks "
                "FROM students WHERE email = ?",
                (email,)
            ).fetchone()

        if student:
            print(
                f"ID: {student[0]} | Name: {student[1]} | "
                f"Email: {student[2]} | Marks: {student[3]:.2f}"
            )
        else:
            print("No student found with that email.")

    except sqlite3.Error:
        print("Unable to search student records.")


def main():
    initialize_database()

    while True:
        print("\n===== Secure Student Management System =====")
        print("1. Add student")
        print("2. View students")
        print("3. Search student")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                name = input("Enter student name: ")
                email = input("Enter student email: ")
                marks = input("Enter marks (0-100): ")

                add_student(name, email, marks)

            elif choice == "2":
                view_students()

            elif choice == "3":
                email = input("Enter student email to search: ")
                search_student(email)

            elif choice == "4":
                print("Application closed.")
                break

            else:
                print("Invalid choice. Select 1, 2, 3, or 4.")

        except ValueError as error:
            print(f"Invalid input: {error}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, sqlite3.Error):
        print("The application could not complete a database operation.")

