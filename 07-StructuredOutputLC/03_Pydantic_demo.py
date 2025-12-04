from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class Student(BaseModel):
    name: str = 'Ahmed'  # if nothing set, it return default Ahmed
    age: Optional[int] = None  # if nothing set it returns None
    email: EmailStr
    cgpa: float = Field(gt=0, lt=10, default=5,
                        description="Decimal value representing the cgpa of the student.")  # constraints and also can apply default value


new_student = {'age': "32",
               'email': 'ahmed@gmail.com'}  # even if age passed as string, pydantic coarce covert it to relevant data type for age
student = Student(**new_student)
# print(student)
student_dict = dict(student)
print(student_dict['name'])
print(student_dict['age'])
print(student_dict['email'])
print(student_dict['cgpa'])

student_json = student.model_dump_json()
print(student_json)
