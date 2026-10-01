Yes. I want to upgrade the earlier **Student Registry** idea into something that actually feels like a small backend service **without having a backend**.

# Project: **Campus Course & Enrollment Manager**

You're going to build a local Python application that receives **API-style JSON payloads**, validates them with Pydantic, applies a few business rules, maintains data in memory, and produces **API-style JSON responses**.

The point is not to build a huge application. The point is to create one project where you naturally use everything you just learned.

Pydantic's model-validation and serialization APIs are designed around this kind of boundary between external data and typed Python models. ([Pydantic Docs](https://docs.pydantic.dev/fastui/api/python_components/?utm_source=chatgpt.com "Python Components - FastUI"))

---

# 1. What are we building?

Imagine a university has a small course enrollment system.

Students can:

- register
    
- update their information
    
- enroll in courses
    
- view their profile
    
- view their enrollments
    

There is **no FastAPI** and **no database**.

Instead:

```text
JSON input
    ↓
Pydantic
    ↓
Validated Python models
    ↓
Application logic
    ↓
Pydantic serialization
    ↓
JSON output
```

This is intentionally shaped like a backend because later, when you learn FastAPI, the HTTP layer will sit around almost exactly this kind of model/validation workflow.

---

# 2. What you will build

Create:

```text
pydantic/
└── 7_campus_manager/
    ├── models.py
    ├── service.py
    ├── data.json
    ├── main.py
    └── README.md
```

Don't worry about making a huge architecture. This is a learning project.

---

# 3. The domain

There are **three main entities**.

## `Address`

```text
city
state
pincode
```

Example external JSON:

```json
{
    "city": "Mumbai",
    "state": "Maharashtra",
    "pincode": "400001"
}
```

---

## `Course`

A course contains:

```text
course_id
course_name
credits
capacity
```

Example:

```json
{
    "courseId": 101,
    "courseName": "Database Management Systems",
    "credits": 4,
    "capacity": 60
}
```

---

## `Student`

A student contains:

```text
student_id
first_name
last_name
age
email
address
enrolled_courses
```

Example:

```json
{
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
    "enrolledCourses": [101, 102]
}
```

Notice that you have:

- aliases
    
- nested models
    
- lists
    
- optional/default values
    
- validation
    
- serialization
    

already appearing naturally.

---

# 4. Pydantic requirements

This is the important part.

You are **required** to use the concepts you've just learned.

## A. Nested models

`Student.address` must be an `Address` model.

So you should end up with something conceptually like:

```text
Student
 ├── student_id
 ├── first_name
 ├── last_name
 ├── age
 ├── email
 └── address
       ├── city
       ├── state
       └── pincode
```

This forces you to use nested Pydantic validation rather than manually checking dictionaries.

---

# 5. Aliases

Your external JSON should use camelCase.

Your Python models should use snake_case.

Use aliases for at least:

```text
student_id  ↔ studentId
first_name  ↔ firstName
last_name   ↔ lastName
course_id   ↔ courseId
course_name ↔ courseName
enrolled_courses ↔ enrolledCourses
```

So internally:

```python
student.first_name
```

Externally:

```json
"firstName"
```

When exporting data, you should deliberately choose whether you want:

```python
model_dump()
```

or:

```python
model_dump(by_alias=True)
```

This is one of the central objectives of the project.

---

# 6. Validation rules

I don't want you to just create models with types.

Add actual rules.

### Student

`age`:

```text
18 <= age <= 100
```

`first_name`:

Convert it to uppercase.

So:

```text
"Ishaan"
```

becomes:

```text
"ISHAAN"
```

`email`:

Must be a valid email.

---

### Address

`pincode`:

Must contain exactly **6 digits**.

---

### Course

`credits`:

```text
1 <= credits <= 6
```

`capacity`:

Must be greater than zero.

---

# 7. Model configuration

Use `ConfigDict`.

I want you to deliberately make an architectural decision here.

For your primary request models:

```text
extra = "forbid"
```

because unknown incoming fields should be considered invalid.

For example:

```json
{
    "studentId": 1,
    "firstName": "Ishaan",
    "lastName": "Sharma",
    "age": 21,
    "email": "ishaan@example.com",
    "address": {...},
    "password": "123456"
}
```

should fail because `password` isn't part of the Student contract.

Also use:

```text
strict = False
```

so something like:

```json
"age": "21"
```

can be converted to the correct Python type.

This gives you a reason to use the configuration instead of putting `ConfigDict` in the project merely because I told you to.

---

# 8. Your service layer

Now comes the part that makes this a **project** instead of a Pydantic exercise.

Create a `CampusManager` class.

It maintains:

```text
students
courses
```

in memory.

For example:

```text
students = [...]
courses = [...]
```

Don't use a database.

---

# 9. Required operations

Your manager should support these operations.

## Register student

Input:

```text
Python dict
```

Process:

```text
dict
 ↓
Student.model_validate()
 ↓
Student
 ↓
store in memory
```

Reject:

- duplicate student IDs
    
- invalid student data
    

---

## Add course

Same idea.

```text
dict
 ↓
Course.model_validate()
 ↓
Course object
 ↓
store
```

Reject duplicate course IDs.

---

## Enroll student

The operation should take:

```text
student_id
course_id
```

and enforce these business rules:

### Rule 1

Student must exist.

### Rule 2

Course must exist.

### Rule 3

Student cannot enroll in the same course twice.

### Rule 4

Course cannot exceed capacity.

This is important:

> These aren't necessarily Pydantic field-validation rules.

They're **application/business rules**.

I want you to start seeing the difference.

```text
Pydantic
    ↓
"Is this data structurally valid?"

Service layer
    ↓
"Is this operation allowed?"
```

That distinction is extremely important when you eventually work on real backends.

---

# 10. Update student

This is where `exclude_unset` gets a practical reason to exist.

Create an update model conceptually containing optional fields:

```text
first_name
last_name
age
email
address
```

All optional.

Then somebody can send:

```json
{
    "age": 22
}
```

without sending every other field.

Your service should determine which fields were actually supplied.

This is where:

```python
model_dump(exclude_unset=True)
```

becomes useful.

For example:

```text
existing student
       +
fields actually supplied
       ↓
updated student
```

The important challenge:

```json
{
    "email": null
}
```

and:

```json
{}
```

should **not** mean the same thing.

That is exactly the distinction you learned between:

```text
exclude_none
```

and:

```text
exclude_unset
```

---

# 11. ValidationError handling

Your application should **not crash** when somebody enters bad data.

Wrap model validation in appropriate `try/except` blocks.

For example:

```text
User input
   ↓
ValidationError
   ↓
extract errors
   ↓
display useful messages
```

When validation fails, show at least:

```text
field/location
message
bad input
```

So the application might display:

```text
Validation failed:

age:
  Value must be between 18 and 100
  received: 15

email:
  Invalid email format
  received: "hello"

extra field:
  password is not permitted
```

You don't have to reproduce exactly that wording; the requirement is to use the structured validation information.

---

# 12. JSON import/export

Now we bring serialization into the project properly.

Have a:

```text
data.json
```

file containing several students and courses.

Your program should be able to:

### Load

```text
data.json
 ↓
JSON string/dict
 ↓
Pydantic models
```

For the JSON-string portion, deliberately use:

```python
model_validate_json()
```

at least once.

---

### Export

Your manager should be able to export its current state back to JSON.

The exported structure should use the **external camelCase aliases**, not the Python field names.

So the output should look like:

```json
{
    "students": [
        {
            "studentId": 1,
            "firstName": "ISHAAN",
            "lastName": "SHARMA"
        }
    ]
}
```

rather than:

```json
{
    "student_id": 1,
    "first_name": "ISHAAN"
}
```

That forces you to use:

```text
model_dump(by_alias=True)
model_dump_json(by_alias=True)
```

for an actual reason.

---

# 13. One extra challenge: `from_attributes`

I want you to use the final configuration concept in a controlled way.

Create a tiny ordinary Python class:

```text
LegacyStudent
```

It should contain attributes such as:

```text
student_id
first_name
last_name
age
email
```

It is **not** a Pydantic model.

Then create a Student model from that object using attribute-based validation.

This gives you an actual reason to understand:

```text
from_attributes=True
```

instead of simply memorizing what it does.

You don't need any ORM or database.

---

# 14. `main.py`

Your `main.py` should act like a tiny command-line application.

Something along the lines of:

```text
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
```

You don't need to make the CLI beautiful.

The **logic** is the point.

---

# 15. What the application should demonstrate

When I'm reviewing your project, I want to be able to find all of these:

|Concept|Where it should appear|
|---|---|
|`BaseModel`|all domain models|
|Nested model|`Student → Address`|
|`Field()`|constraints|
|`field_validator`|name/email/format validation|
|`model_validator`|at least one cross-field rule|
|`computed_field`|something useful such as display name|
|`model_validate()`|dict → model|
|`model_validate_json()`|JSON → model|
|`ValidationError`|invalid input handling|
|`.errors()`|readable error reporting|
|`ConfigDict`|model behavior|
|`extra="forbid"`|request contract|
|`strict=False`|coercion|
|`from_attributes=True`|legacy object conversion|
|`Field(alias=...)`|camelCase external schema|
|`model_dump()`|internal Python representation|
|`model_dump(by_alias=True)`|external representation|
|`model_dump_json()`|JSON export|
|`exclude_unset=True`|partial student updates|
|`exclude_none=True`|clean output|

That's a **very good integration exercise** because every Pydantic feature has a reason to exist.

---

# 16. One useful `computed_field`

Since you've already learned `computed_field`, don't let it become dead knowledge.

Give Student:

```text
display_name
```

computed from:

```text
first_name + last_name
```

For example:

```text
ISHAAN SHARMA
```

Your exported representation can therefore demonstrate that computed fields are included in serialization by default unless you explicitly change the serialization behavior.

---

# 17. One useful `model_validator`

Create one cross-field rule.

For example:

> A student younger than 18 cannot be registered.

However, since you already have `age >= 18` as a field constraint, that would be redundant.

So instead use something like:

> If a student is enrolled in more than 5 courses, registration should fail.

Or:

> If a course has more than 4 credits, its capacity must be at least 10.

The point is to require looking at **multiple fields together**.

That gives `model_validator` a legitimate job.

---

# 18. What you should NOT build

Don't accidentally turn this into a month-long project.

No:

- FastAPI
    
- Flask
    
- Django
    
- SQLAlchemy
    
- PostgreSQL
    
- frontend
    
- authentication
    
- REST server
    
- Docker
    
- deployment
    
- GUI
    

This is a **Pydantic integration laboratory**.

The only persistence is a simple JSON file.

---

# 19. Definition of done

I will consider you finished when your program can successfully do this:

```text
1. Take external camelCase data
              ↓
2. Validate it
              ↓
3. Convert it into Python models
              ↓
4. Enforce field + cross-field rules
              ↓
5. Store models in memory
              ↓
6. Perform business operations
              ↓
7. Handle invalid data without crashing
              ↓
8. Update only fields supplied by the user
              ↓
9. Convert models back to camelCase data
              ↓
10. Export valid JSON
```

And you should be able to explain **why every Pydantic feature is being used**.

---

# 20. How I want you to approach it

Don't build the entire thing in one giant file.

Build it in stages:

```text
Phase 1
Models
    ↓
Phase 2
Validation
    ↓
Phase 3
Service/business logic
    ↓
Phase 4
JSON import/export
    ↓
Phase 5
CLI
    ↓
Phase 6
Error handling
    ↓
Phase 7
Testing
```

A reasonable target is **1.5–2.5 hours**, depending on how much you code yourself.

And one rule from professor mode:

> **Don't copy a finished Pydantic project from the internet.**

You already know enough of the building blocks. The value now is forcing your brain to decide **which Pydantic feature belongs where**.

When you're finished, paste the project code here. I'll review it against the requirements above and tell you exactly which parts demonstrate real understanding versus which parts are merely syntactically correct.Yes. I want to upgrade the earlier **Student Registry** idea into something that actually feels like a small backend service **without having a backend**.