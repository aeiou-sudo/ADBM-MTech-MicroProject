import sqlite3

class Database:
    def __init__(self, db_name="students.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.setup_table()
    
    def setup_table(self):
        # Create a table for student details
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_number TEXT NOT NULL UNIQUE,
                department TEXT NOT NULL
            );
        """)
        self.connection.commit()

    def insert_student(self, name, roll_number, department):
        try:
            self.cursor.execute("""
                INSERT INTO students (name, roll_number, department)
                VALUES (?, ?, ?);
            """, (name, roll_number, department))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def fetch_all_students(self):
        self.cursor.execute("SELECT * FROM students;")
        return self.cursor.fetchall()
