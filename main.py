import json
from pydantic import ValidationError

from service import CampusManager


manager = CampusManager()
manager.import_data()


def print_student(student):
    print(json.dumps(student.model_dump(by_alias=True), indent=4))


def print_course(course):
    print(json.dumps(course.model_dump(by_alias=True), indent=4))


while True:

    print("""
=================================
Campus Course Manager
=================================
1. Add student
2. Add course
3. Enroll student
4. Update student
5. View student
6. View course
7. Export data
8. Exit
""")

    try:
        choice = int(input("Enter your choice: "))

    except ValueError:
        print("Please enter a number from 1 to 8.")
        continue

    if choice == 1:

        try:
            student_id = int(input("Enter student ID: "))
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            age = int(input("Enter age: "))
            email = input("Enter email: ")

            city = input("Enter city: ")
            state = input("Enter state: ")
            pincode = input("Enter pincode: ")

            address = {
                "city": city,
                "state": state,
                "pincode": pincode
            }

            course_input = input(
                "Enter enrolled course IDs separated by spaces "
                "(press Enter for none): "
            )

            if course_input.strip():
                enrolled_courses = [
                    int(course_id)
                    for course_id in course_input.split()
                ]
            else:
                enrolled_courses = []

            student_data = {
                "studentId": student_id,
                "firstName": first_name,
                "lastName": last_name,
                "age": age,
                "email": email,
                "address": address,
                "enrolledCourses": enrolled_courses
            }

            manager.register_student(student_data)

            print("Student registered successfully.")

        except (ValueError, ValidationError) as e:
            print("Could not register student.")
            print(e)

    elif choice == 2:

        try:
            course_id = int(input("Enter course ID: "))
            course_name = input("Enter course name: ")
            credits = int(input("Enter credits: "))
            capacity = int(input("Enter capacity: "))

            course_data = {
                "courseId": course_id,
                "courseName": course_name,
                "credits": credits,
                "capacity": capacity
            }

            manager.add_course(course_data)

            print("Course added successfully.")

        except (ValueError, ValidationError) as e:
            print("Could not add course.")
            print(e)

    elif choice == 3:

        try:
            student_id = int(input("Enter student ID: "))
            course_id = int(input("Enter course ID: "))

            result = manager.enroll_student(student_id, course_id)

            print(result)

        except ValueError as e:
            print("Enrollment failed.")
            print(e)

    elif choice == 4:

        try:
            student_id = int(input("Enter student ID: "))

            update_data = {}

            first_name = input(
                "New first name (press Enter to keep current): "
            )
            if first_name.strip():
                update_data["firstName"] = first_name

            last_name = input(
                "New last name (press Enter to keep current): "
            )
            if last_name.strip():
                update_data["lastName"] = last_name

            age = input(
                "New age (press Enter to keep current): "
            )
            if age.strip():
                update_data["age"] = int(age)

            email = input(
                "New email (press Enter to keep current): "
            )
            if email.strip():
                update_data["email"] = email

            change_address = input(
                "Do you want to update the address? (y/n): "
            )

            if change_address.lower() == "y":
                city = input("New city: ")
                state = input("New state: ")
                pincode = input("New pincode: ")

                update_data["address"] = {
                    "city": city,
                    "state": state,
                    "pincode": pincode
                }

            updated_student = manager.update_student(
                student_id,
                update_data
            )

            print("Student updated successfully.")
            print_student(updated_student)

        except (ValueError, ValidationError) as e:
            print("Could not update student.")
            print(e)

    elif choice == 5:

        try:
            student_id = int(input("Enter student ID: "))

            student = manager.get_student(student_id)

            print_student(student)

        except ValueError as e:
            print(e)

    elif choice == 6:

        try:
            course_id = int(input("Enter course ID: "))

            course = manager.get_course(course_id)

            print_course(course)

        except ValueError as e:
            print(e)

    elif choice == 7:

        try:
            manager.bothexport()
            print("Data exported successfully to data.json.")

        except Exception as e:
            print("Export failed.")
            print(e)

    elif choice == 8:

        print("Exiting...")
        break

    else:
        print("Invalid choice. Enter a number from 1 to 8.")