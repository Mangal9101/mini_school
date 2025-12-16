from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from auth import hash_password   

def create_default_principal():
    db: Session = SessionLocal()

    principal = db.query(User).filter(User.role == "principal").first()

    if not principal:
        user = User(
            username="Mangal",
            password=hash_password("Mangal123"),
            role="principal"
        )
        db.add(user)
        db.commit()

    db.close()
