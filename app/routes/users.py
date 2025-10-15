from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from app.database import get_session
from app.models.models import User, Borrow, Book

router = APIRouter(prefix="/users", tags=["users"])
templates = Jinja2Templates(directory="app/templates")

@router.get('/{user_id}/dashboard')
async def user_dashboard(request: Request, user_id: int):
    with next(get_session()) as session:
        user = session.get(User, user_id)
        borrows = session.exec(select(Borrow).where(Borrow.user_id == user_id)).all()
        detailed = []
        for b in borrows:
            book = session.get(Book, b.book_id)
            detailed.append({'borrow': b, 'book': book})
        return templates.TemplateResponse('user_dashboard.html', {'request': request, 'user': user, 'borrows': detailed})

@router.get('/admin')
async def admin_dashboard(request: Request):
    with next(get_session()) as session:
        users = session.exec(select(User)).all()
        books = session.exec(select(Book)).all()
        borrows = session.exec(select(Borrow)).all()
        return templates.TemplateResponse('admin_dashboard.html', {'request': request, 'users': users, 'books': books, 'borrows': borrows})
________________________________________
main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import init_db
from app.routes import auth, books, users

app = FastAPI()

# mount static and templates are used from routes
app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(users.router)

@app.on_event('startup')
async def startup_event():
    init_db()

@app.get('/')
async def home(request: Request):
    templates = Jinja2Templates(directory='app/templates')
    return templates.TemplateResponse('books_list.html', {'request': request, 'books': []})
