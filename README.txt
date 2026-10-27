YUVAINTERN WEEK 5 - SECURITY ENHANCEMENTS IN PYTHON APPLICATIONS

Project Name: Secure Student Management System

Description:
This project demonstrates security improvements in a Python application using SQLite.

Files:
1. secure_student_app.py - Main Python application.
2. test_security.py - Automated security testing using unittest.
3. YuvaIntern_Week5_Security_Audit_Report.docx - Security audit report.
4. README.txt - Project instructions and information.

Security Features:
- Input validation for names, email addresses, and marks.
- Parameterized SQL queries to reduce SQL injection risks.
- Database constraints to prevent duplicate emails and invalid marks.
- Error handling to avoid exposing internal database details.
- Automated tests for validation and database behavior.

How to Run:
1. Install Python 3.10 or later.
2. Open a terminal in the project folder.
3. Run: python secure_student_app.py

How to Run Security Tests:
Run: python -m unittest -v test_security.py

Limitations:
Authentication, authorization, and database encryption are not implemented. This project is an educational demonstration and should not store real sensitive student information.