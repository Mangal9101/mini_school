from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import verify_password, create_access_token

router = APIRouter()


@router.get("/")
def home(request: Request):
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("home.html", {"request": request})


@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        return RedirectResponse("/", status_code=302)

    token = create_access_token({"sub": user.username})
    response = RedirectResponse(
        "/principal/dashboard" if user.role == "principal" else "/teacher/dashboard",
        status_code=302
    )
    response.set_cookie("access_token", token, httponly=True)
    return response
