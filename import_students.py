import pandas as pd
import sqlite3
from bloom_filter import ExtensibleBloomFilter

class CSVToDatabase:
    def __init__(self, db_name="students.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.setup_table()

    def setup_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                gender TEXT NOT NULL,
                part_time_job BOOLEAN NOT NULL,
                absence_days INTEGER NOT NULL,
                extracurricular_activities BOOLEAN NOT NULL,
                weekly_self_study_hours INTEGER NOT NULL,
                career_aspiration TEXT NOT NULL,
                math_score INTEGER NOT NULL,
                history_score INTEGER NOT NULL,
                physics_score INTEGER NOT NULL,
                chemistry_score INTEGER NOT NULL,
                biology_score INTEGER NOT NULL,
                english_score INTEGER NOT NULL,
                geography_score INTEGER NOT NULL
            );
        """)
        self.connection.commit()

    def insert_student(self, student_data):
        try:
            self.cursor.execute("""
                INSERT INTO students (
                    first_name, last_name, email, gender, part_time_job, absence_days,
                    extracurricular_activities, weekly_self_study_hours, career_aspiration,
                    math_score, history_score, physics_score, chemistry_score, biology_score,
                    english_score, geography_score
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, student_data)
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error inserting data: {e}")

    def import_from_csv(self, csv_file):
        try:
            # Read CSV file using pandas
            data = pd.read_csv(csv_file)

            # Standardize column names
            data.columns = data.columns.str.strip().str.lower().str.replace(" ", "_")

            # Clean and map boolean columns for part_time_job
            data["part_time_job"] = data["part_time_job"].apply(
                lambda x: True if str(x).strip().lower() == "true" else 
                        False if str(x).strip().lower() == "false" else None
            ).fillna(False)  # Default to False for missing/invalid values

            # Clean and map boolean columns for extracurricular_activities
            data["extracurricular_activities"] = data["extracurricular_activities"].apply(
                lambda x: True if str(x).strip().lower() == "true" else 
                        False if str(x).strip().lower() == "false" else None
            ).fillna(False)  # Default to False for missing/invalid values

            # Insert each row into the database
            for _, row in data.iterrows():
                student_data = (
                    row["first_name"], row["last_name"], row["email"], row["gender"],
                    row["part_time_job"], int(row["absence_days"]),
                    row["extracurricular_activities"], int(row["weekly_self_study_hours"]),
                    row["career_aspiration"], int(row["math_score"]), int(row["history_score"]),
                    int(row["physics_score"]), int(row["chemistry_score"]), int(row["biology_score"]),
                    int(row["english_score"]), int(row["geography_score"])
                )
                self.insert_student(student_data)

            print("CSV data has been imported successfully.")
        except Exception as e:
            print(f"Error processing CSV file: {e}")


if __name__ == "__main__":
    db = CSVToDatabase()
    csv_file_path = "students_edited.csv"  # Replace with your actual CSV file path
    db.import_from_csv(csv_file_path)
