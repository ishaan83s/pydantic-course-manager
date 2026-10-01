from service import CampusManager

# 1. Create manager
manager = CampusManager()

# 2. Add a student
manager.register_student({
    "studentId": 1,
    "firstName": "Ishaan",
    "lastName": "Sharma",
    "age": 21,
    "email": "ishaan@example.com",
    "address": {
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400001"
    },
    "enrolledCourses": []
})

# 3. Add a course
manager.add_course({
    "courseId": 101,
    "courseName": "Database Management Systems",
    "credits": 4,
    "capacity": 2
})

# 4. Export everything
manager.bothexport()

print("Export completed.")

fresh_manager = CampusManager()

fresh_manager.import_data()

print(fresh_manager.student)
print(fresh_manager.course)

