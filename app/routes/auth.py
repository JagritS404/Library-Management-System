from fastapi import APIRouter, Request, Form, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.utils.security import hash_password, verify_password, create_access_token
from app.database import get_session
from sqlmodel import Session, select
from app.models.models import User
from config import settings
from typing import Optional


router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="app/templates")


@router.get('/login')
async def login_page(request: Request):
return templates.TemplateResponse('login.html', {'request': request})


@router.post('/login')
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
with next(get_session()) as session:
stmt = select(User).where(User.email == email)
user = session.exec(stmt).first()
if not user or not user.hashed_password or not verify_password(password, user.hashed_password):
raise HTTPException(status_code=401, detail='Invalid credentials')
token = create_access_token(subject=str(user.id))
response = RedirectResponse(url='/', status_code=302)
response.set_cookie('access_token', token, httponly=True)
return response


@router.post('/register')
async def register(request: Request, email: str = Form(...), name: Optional[str] = Form(None), password: Optional[str] = Form(None)):
with next(get_session()) as session:
stmt = select(User).where(User.email == email)
if session.exec(stmt).first():
raise HTTPException(status_code=400, detail='User already exists')
user = User(email=email, name=name, hashed_password=hash_password(password) if password else None)
session.add(user)
session.commit()
session.refresh(user)
token = create_access_token(subject=str(user.id))
response = RedirectResponse(url='/', status_code=302)
response.set_cookie('access_token', token, httponly=True)
return response