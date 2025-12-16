from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from models import User,Student
from auth import verify_password, create_access_token
from dependencies import teacher_required,principal_required
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/teacher", tags=["Teacher"])


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        "teacher_login.html",  
        {"request": request}
    )

@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    teacher = db.query(User).filter(User.username == username, User.role == "teacher").first()
    if not teacher or not verify_password(password, teacher.password):
         return templates.TemplateResponse("teacher_login.html", {"request": request, "error": "Invalid credentials"})

    token = create_access_token({"sub": teacher.username, "role": "teacher"})
    response = RedirectResponse(url="/teacher/dashboard", status_code=302)
    response.set_cookie("access_token", f"Bearer {token}", httponly=True)
    return response

@router.get("/dashboard")
def dashboard(request: Request, user=Depends(teacher_required)):
    return templates.TemplateResponse(
        "teacher_dashboard.html", 
        {"request": request, "user": user}
    )


@router.get("/add-student")
def add_student_page(request: Request, user=Depends(teacher_required)):
    return templates.TemplateResponse(
        "add_student.html",
        {"request": request}
    )

@router.post("/add-student")
def add_student(roll_no: str = Form(...),name: str = Form(...),course: str = Form(...),fees: str = Form(...),address: str = Form(...),contact_no: str = Form(...),
                db: Session = Depends(get_db),user=Depends(teacher_required)
):
    student = Student(
        roll_no=roll_no,
        name=name,
        course=course,
        fees=fees,
        address=address,
        contact_no=contact_no
    )
    db.add(student)
    db.commit()
    return RedirectResponse("/teacher/students", status_code=302)

@router.get("/students")
def student_list(request: Request, db: Session = Depends(get_db), user=Depends(teacher_required)):
    students = db.query(Student).all()
    return templates.TemplateResponse(
        "teacher_student_list.html",
        {"request": request, "students": students}
    )

@router.get("/students/t-edit/{student_no}")
def edit_student_page(student_no: str, request: Request, db: Session = Depends(get_db), user=Depends(teacher_required)):
    student = db.query(Student).filter(Student.roll_no == student_no).first()
    if not student:
        raise HTTPException(404, "Student not found")
    return templates.TemplateResponse("t_edit_student.html", {"request": request, "student": student})

@router.post("/students/t-edit/{student_no}")
def edit_student(student_no: str,name: str = Form(...),course: str = Form(...),fees: str = Form(...),address: str = Form(...),contact_no: str = Form(...),db: Session = Depends(get_db),user = Depends(teacher_required)):
    student = db.query(Student).filter(Student.roll_no == student_no).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.name = name
    student.course = course
    student.fees = fees
    student.address = address
    student.contact_no = contact_no

    db.commit()
    return RedirectResponse("/teacher/students", status_code=303)


    