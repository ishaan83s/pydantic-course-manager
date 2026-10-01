from pydantic import BaseModel,Field,EmailStr,AnyUrl,ValidationError,ConfigDict,field_validator,computed_field,model_validator
from typing import Annotated,Optional,List,Dict
from model import Student,Course,StudentUpdate
import json

class CampusManager:
    def __init__(self):
        self.student = {}
        self.course = {}

    def register_student(self, data):
        student = Student.model_validate(data)

        if student.student_id in self.student:
            raise ValueError("Student ID cannot be duplicate.")
        
        self.student[student.student_id] = student

    def add_course(self,data):
        course = Course.model_validate(data)

        if course.course_id in self.course:
            raise ValueError("Course ID cannot be duplicate.")

        self.course[course.course_id] = course

    def enroll_student(self,student_id,course_id):

        if student_id not in self.student:
            raise ValueError("Student doesnt exist, Register the student first.")

        if course_id not in self.course:
            raise ValueError("Invalid Course")

        student = self.student[student_id]
        
        if course_id in student.enrolled_courses:
            raise ValueError("Student already registered for this course.")  


        enrolled_count = 0

        for current_student in self.student.values():
            if course_id in current_student.enrolled_courses :
                enrolled_count += 1

        if enrolled_count >= self.course[course_id].capacity:
            raise ValueError("Course seats are full")

        student.enrolled_courses.append(course_id)

        return {
            "success": True
        }

    def update_student(self,student_id,data): 

        if student_id not in self.student:
            raise ValueError("Student doesnt exist")

        update = StudentUpdate.model_validate(data) #a dictionary containing only the fields the user actually supplied.
        changes = update.model_dump(exclude_unset=True) #MODEL THAT HAS FILTERED DATA
        
        student = self.student[student_id]

        for field , value in changes.items():
            setattr(student,field,value) #object #thing to change #value

        return student

    def get_student(self,student_id):
        if student_id not in self.student:
            raise ValueError("Student doesnt exist")
        student = self.student[student_id]
        return student
    

    def get_course(self, course_id):
        if course_id not in self.course:
            raise ValueError("Course doesnt exist")
        course = self.course[course_id]
        return course

    def exportstudents(self):
        students = []
        for student_id in self.student:
            student = self.student[student_id]
            students.append(student.model_dump(by_alias=True))
        return students

    def exportcourses(self):
        courses=[]
        for course_id in self.course:
            course = self.course[course_id]
            courses.append(course.model_dump(by_alias= True))
        return courses

    def bothexport(self):
        students_data = self.exportstudents()
        courses_data = self.exportcourses()

        data = {
            "students" : students_data,
            "courses" : courses_data
        }

        with open("pydantic2/project/7_campus_manager/data.json", "w") as file:
            json.dump(data,file,indent=4)

        return data

    def import_data(self):
        with open("pydantic2/project/7_campus_manager/data.json", "r") as file:
            data = json.load(file)

            students_data = data["students"]
            course_data = data["courses"]

        for one_student_data in students_data:
            one_student_data.pop("full_name",None)
            student_json = json.dumps(one_student_data)
            student = Student.model_validate_json(student_json)
            
            if student.student_id not in self.student:
                self.student[student.student_id] = student

        for one_course_data in course_data:
            course_json = json.dumps(one_course_data)
            course = Course.model_validate_json(course_json)
            if course.course_id not in self.course:
                self.course[course.course_id] = course        
