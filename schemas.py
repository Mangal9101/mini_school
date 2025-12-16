from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    role: str


class StudentBase(BaseModel):
    roll_no: str
    name: str
    course: str
    fees: str
    address: str
    contact_no: str


class StudentCreate(StudentBase):
    pass
