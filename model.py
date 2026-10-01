from pydantic import BaseModel,Field,EmailStr,AnyUrl,ValidationError,ConfigDict,field_validator,computed_field,model_validator
from typing import Annotated,Optional,List,Dict

class Address(BaseModel):
    model_config=ConfigDict(extra="forbid",strict=False)
    city : str = Field(max_length=25,alias="city")
    state : str = Field(max_length=25,alias="state")
    pincode : str = Field(pattern=r"^\d{6}$")

class Course(BaseModel):
    model_config=ConfigDict(extra="forbid",strict=False)
    course_id : int = Field(alias="courseId")
    course_name : str = Field(alias="courseName")
    credits : int = Field(gt=0 ,lt=7)
    capacity : int = Field(gt=0)

# #credits > 4
#       ↓
# capacity must be >= 10

    @model_validator(mode = "after")
    def validate_capacity(self):
        if self.credits > 4 and self.capacity < 10:
            raise ValueError("If Credits are Greater than 4 ,then Capacity must be Atleast 10")
        return self

class Student(BaseModel):
    model_config=ConfigDict(extra="forbid",strict=False,from_attributes=True)
    student_id:int = Field(alias="studentId")
    first_name:str = Field(alias="firstName")
    last_name:str = Field(alias="lastName")
    age:int = Field(gt=17,lt=101)
    email:EmailStr
    address:Address
    enrolled_courses: List[int] = Field(alias="enrolledCourses")

    @field_validator("first_name","last_name") 
    @classmethod
    def transform_name(cls, value):
        return value.upper()

    @computed_field()
    @property
    def full_name(self)->str:
        return f"{self.first_name} {self.last_name}"


class StudentUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid",strict=False)
    first_name : Annotated[Optional[str],Field(alias="firstName")] = None
    last_name : Annotated[Optional[str],Field(alias="lastName")] = None
    age : Annotated[Optional[int],Field(gt=17,lt=101)] = None
    email: Optional[EmailStr]= None
    address: Optional[Address] = None


class LegacyStudent:

    def __init__(self, student_id, first_name, last_name, age, email , address , enrolled_courses):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.address = address
        self.enrolled_courses = enrolled_courses

legacy = LegacyStudent(
    1,
    "Ishaan",
    "Sharma",
    21,
    "ishaan@example.com",
{
    "city": "Mumbai",
    "state": "Maharashtra",
    "pincode": "400001",
},
    []

)
try :
    legacy = Student.model_validate(legacy,by_name= True)
except ValidationError as e:
    print(e.errors())

print(legacy)
print(type(legacy))