from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from models import User, Student
from auth import hash_password
from dependencies import principal_required
from auth import create_access_token, verify_password
from fastapi import HTTPException

router = APIRouter(prefix="/principal", tags=["Principal"])
templates = Jinja2Templates(directory="templates")


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("principal_login.html", {"request": request})

@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    principal = db.query(User).filter(User.username == username, User.role == "principal").first()
    if not principal or not verify_password(password, principal.password):
         return templates.TemplateResponse("principal_login.html", {"request": request, "error": "Invalid credentials"})
    token = create_access_token({"sub": principal.username, "role": "principal"})
    response = RedirectResponse(url="/principal/dashboard", status_code=302)
    response.set_cookie("access_token", f"Bearer {token}", httponly=True)
    return response

@router.get("/dashboard")
def dashboard(request: Request, user=Depends(principal_required)):
    return templates.TemplateResponse(
        "principal_dashboard.html", 
        {"request": request, "user": user}
    )


@router.get("/dashboard")
def dashboard(
    request: Request,
    user=Depends(principal_required)
):
    return templates.TemplateResponse("principal_dashboard.html", {"request": request})


@router.get("/add-teacher")
def add_teacher_page(request: Request, user=Depends(principal_required)):
    return templates.TemplateResponse("add_teacher.html", {"request": request})


@router.post("/add-teacher")
def add_teacher(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
    user=Depends(principal_required)
):
    teacher = User(
        username=username,
        password=hash_password(password),
        role="teacher"
    )
    db.add(teacher)
    db.commit()
    return RedirectResponse("/principal/teachers", status_code=302)



@router.get("/teachers")
def teacher_list(request: Request, db: Session = Depends(get_db), user=Depends(principal_required)):
    teachers = db.query(User).filter(User.role == "teacher").all()
    return templates.TemplateResponse("teacher_list.html", {"request": request, "teachers": teachers})

@router.get("/teachers/add")
def add_teacher_page(request: Request, user=Depends(principal_required)):
    return templates.TemplateResponse("add_teacher.html", {"request": request})

@router.post("/teachers/add")
def add_teacher(username: str = Form(...), password: str = Form(...),
                db: Session = Depends(get_db), user=Depends(principal_required)):
    teacher = User(username=username, password=hash_password(password), role="teacher")
    db.add(teacher)
    db.commit()
    return RedirectResponse("/principal/teachers", status_code=302)

@router.get("/teachers/edit/{teacher_id}")
def edit_teacher_page(teacher_id: int, request: Request, db: Session = Depends(get_db), user=Depends(principal_required)):
    teacher = db.query(User).filter(User.id == teacher_id, User.role=="teacher").first()
    if not teacher:
        raise HTTPException(404, "Teacher not found")
    return templates.TemplateResponse("edit_teacher.html", {"request": request, "teacher": teacher})

@router.post("/teachers/edit/{teacher_id}")
def edit_teacher(teacher_id: int, username: str = Form(...), password: str = Form(...),
                 db: Session = Depends(get_db), user=Depends(principal_required)):
    teacher = db.query(User).filter(User.id == teacher_id, User.role=="teacher").first()
    if not teacher:
        raise HTTPException(404, "Teacher not found")
    teacher.username = username
    if password:
        teacher.password = hash_password(password)
    db.commit()
    return RedirectResponse("/principal/teachers", status_code=302)

@router.get("/teachers/delete/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db), user=Depends(principal_required)):
    teacher = db.query(User).filter(User.id == teacher_id, User.role=="teacher").first()
    if not teacher:
        raise HTTPException(404, "Teacher not found")
    db.delete(teacher)
    db.commit()
    return RedirectResponse("/principal/teachers", status_code=302)


# ----------------------- Students -----------------------
@router.get("/students")
def student_list(request: Request, db: Session = Depends(get_db), user=Depends(principal_required)):
    students = db.query(Student).all()
    return templates.TemplateResponse("student_list.html", {"request": request, "students": students})

@router.get("/students/add")
def add_student_page(request: Request, user=Depends(principal_required)):
    return templates.TemplateResponse("add_student.html", {"request": request})

@router.post("/students/add")
def add_student(name: str = Form(...), roll_no: str = Form(...), course: str = Form(...),
                fees: str = Form(...), address: str = Form(...), contact_no: str = Form(...),
                db: Session = Depends(get_db), user=Depends(principal_required)):
    student = Student(name=name, roll_no=roll_no, course=course, fees=fees,
                      address=address, contact_no=contact_no)
    db.add(student)
    db.commit()
    return RedirectResponse("/principal/students", status_code=302)


@router.get("/students/edit/{student_no}")
def edit_student_page( student_no: str, request: Request, db: Session = Depends(get_db), user=Depends(principal_required) ):
    student = db.query(Student).filter(Student.roll_no == student_no).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return templates.TemplateResponse("edit_student.html", {"request": request, "student": student})

@router.post("/students/edit/{student_no}")
def edit_student(
    student_no: str,
    name: str = Form(...),
    course: str = Form(...),
    fees: str = Form(...),
    address: str = Form(...),
    contact_no: str = Form(...),
    db: Session = Depends(get_db),
    user=Depends(principal_required)
):
    student = db.query(Student).filter(Student.roll_no == student_no).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.name = name
    student.course = course
    student.fees = fees
    student.address = address
    student.contact_no = contact_no

    db.commit()

    return RedirectResponse("/principal/students", status_code=302)

@router.get("/students/delete/{student_no}")
def delete_student(student_no: str, db: Session = Depends(get_db), user=Depends(principal_required)):
    student = db.query(Student).filter(Student.roll_no == student_no).first()
    if not student:
        raise HTTPException(404, "Student not found")
    db.delete(student)
    db.commit()
    return RedirectResponse("/principal/students", status_code=302)

















