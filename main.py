from database import Database
from bloom_filter import ExtensibleBloomFilter

class StudentSystem:
    def __init__(self):
        self.database = Database()
        self.ebf = ExtensibleBloomFilter(initial_size=1024, hash_count=6, false_positive_rate=0.01)

    def add_student(self, name, id, department):
        if self.database.insert_student(name, roll_number, department):
            # Add to EBF automatically
            self.ebf.add(id)
            print(f"Student {name} added successfully!")
        else:
            print(f"Student with roll number {roll_number} already exists!")

    def query_student(self, id):
        if self.ebf.query(id):
            print(f"Roll number {id} might exist in the database (membership check passed).")
        else:
            print(f"Roll number {id} does not exist.")

    def display_students(self):
        students = self.database.fetch_all_students()
        for student in students:
            print(student)


if __name__ == "__main__":
    system = StudentSystem()

    while True:
        print("\n1. Add Student")
        print("2. Query Student")
        print("3. Display All Students")
        print("4. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            name = input("Enter name: ")
            roll_number = input("Enter roll number: ")
            department = input("Enter department: ")
            system.add_student(name, roll_number, department)
        elif choice == "2":
            roll_number = input("Enter roll number: ")
            system.query_student(roll_number)
        elif choice == "3":
            system.display_students()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Try again.")
