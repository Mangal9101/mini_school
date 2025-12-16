from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)  # principal / teacher

    students = relationship("Student", back_populates="teacher")


class Student(Base):
    __tablename__ = "students"

    roll_no = Column(String, unique=True, index=False, primary_key=True)
    name = Column(String)
    course = Column(String)
    fees = Column(String)
    address = Column(String)
    contact_no = Column(String)

    teacher_id = Column(Integer, ForeignKey("users.id"))
    teacher = relationship("User", back_populates="students")
