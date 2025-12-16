from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import SECRET_KEY, ALGORITHM



def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()
    return user


def principal_required(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(401, "Not logged in")
    try:
        payload = jwt.decode(token.replace("Bearer ", ""), SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(401, "Invalid token")
    if payload.get("role") != "principal":
        raise HTTPException(403, "Not authorized")
    return payload



def teacher_required(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(401, "Not logged in")
    try:
        payload = jwt.decode(token.replace("Bearer ", ""), SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    if payload.get("role") != "teacher":
        raise HTTPException(status_code=403, detail="Not authorized")
    return payload