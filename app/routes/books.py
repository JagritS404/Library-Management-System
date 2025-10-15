from fastapi import APIRouter, Request, Depends, UploadFile, File, HTTPException
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from app.database import get_session
from app.models.models import Book, Category, Borrow, User
from app.services.excel_service import parse_books_excel, books_to_excel
from fastapi.responses import StreamingResponse, HTMLResponse
from io import BytesIO

router = APIRouter(prefix="/books", tags=["books"])
templates = Jinja2Templates(directory="app/templates")

@router.get('/')
async def list_books(request: Request):
    with next(get_session()) as session:
        books = session.exec(select(Book)).all()
        return templates.TemplateResponse('books_list.html', {'request': request, 'books': books})

@router.post('/upload')
async def upload_books(file: UploadFile = File(...)):
    content = await file.read()
    parse_books_excel(content)
    return {"status": "uploaded"}

@router.get('/export')
async def export_books():
    with next(get_session()) as session:
        books = session.exec(select(Book)).all()
        buf = books_to_excel(books)
        return StreamingResponse(buf, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers={
            'Content-Disposition': 'attachment; filename=books.xlsx'
        })

@router.post('/{book_id}/borrow')
async def borrow_book(book_id: int, user_id: int):
    with next(get_session()) as session:
        book = session.get(Book, book_id)
        user = session.get(User, user_id)
        if not book or not user:
            raise HTTPException(404, 'Not found')
        if book.copies_available <= 0:
            raise HTTPException(400, 'No copies available')
        borrow = Borrow(user_id=user.id, book_id=book.id)
        book.copies_available -= 1
        session.add(borrow)
        session.add(book)
        session.commit()
        return {"status": "borrowed"}

@router.post('/{book_id}/return')
async def return_book(book_id: int, user_id: int):
    with next(get_session()) as session:
        stmt = select(Borrow).where(Borrow.book_id == book_id, Borrow.user_id == user_id, Borrow.returned_at == None)
        borrow = session.exec(stmt).first()
        if not borrow:
            raise HTTPException(404, 'Borrow record not found')
        borrow.returned_at = __import__('datetime').datetime.utcnow()
        book = session.get(Book, book_id)
        book.copies_available += 1
        session.add(borrow)
        session.add(book)
        session.commit()
        return {"status": "returned"}
