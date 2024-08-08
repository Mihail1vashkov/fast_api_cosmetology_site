from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel
import bcrypt
from database import SessionLocal
from models import User, Service, Appointment

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Главная страница | Косметология"})

@app.get("/procedures")
async def get_procedures(request: Request, db: Session = Depends(get_db)):
    procedures = db.query(Service).all()
    return templates.TemplateResponse("procedures.html", {"request": request, "title": "Процедуры", "procedures": procedures})

@app.get("/analytics")
async def get_analytics(request: Request, db: Session = Depends(get_db)):
    total_records = db.query(Appointment).count()
    avg_procedures_per_client = total_records  # Упростим для примера
    return templates.TemplateResponse("analytics.html", {
        "request": request,
        "title": "Аналитика",
        "total_records": total_records,
        "avg_procedures_per_client": avg_procedures_per_client
    })

@app.get("/search")
async def search(request: Request, query: str = None, db: Session = Depends(get_db)):
    results = []
    if query:
        results = db.query(Service).filter(Service.name.contains(query)).all()
    return templates.TemplateResponse("search_results.html", {"request": request, "results": results, "query": query})

# Раскомментируйте, если хотите добавить аутентификацию
# @app.get("/auth")
# async def auth_page(request: Request):
#     return templates.TemplateResponse("auth.html", {"request": request})

# @app.post("/register")
# async def register(user: UserCreate, db: Session = Depends(get_db)):
#     hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
#     db_user = User(username=user.username, hashed_password=hashed_password.decode('utf-8'))
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return {"message": "User registered successfully"}

# @app.post("/login")
# async def login(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.username == user.username).first()
#     if not db_user or not bcrypt.checkpw(user.password.encode('utf-8'), db_user.hashed_password.encode('utf-8')):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
#     return {"message": "Logged in successfully"}
