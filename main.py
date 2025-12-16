from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import Base, engine
from routers import principal, teacher, auth_routes
from fastapi.templating import Jinja2Templates
import os
from seed import create_default_principal




BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# app.include_router(principal.router, prefix="/principal")
app.include_router(teacher.router, prefix="/teacher")
app.include_router(auth_routes.router)

app.include_router(principal.router)
app.include_router(teacher.router)

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static",)

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    create_default_principal()
