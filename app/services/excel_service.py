import pandas as pd
from io import BytesIO
from app.models.models import Book, Category
from sqlmodel import Session, select
from app.database import engine




def parse_books_excel(file_bytes: bytes):
df = pd.read_excel(BytesIO(file_bytes))
# Expect columns: title,author,isbn,category,copies,description
books = []
with Session(engine) as session:
for _, row in df.iterrows():
cat_name = str(row.get('category', 'Uncategorized'))
stmt = select(Category).where(Category.name == cat_name)
cat = session.exec(stmt).first()
if not cat:
cat = Category(name=cat_name)
session.add(cat)
session.commit()
session.refresh(cat)
book = Book(
title=row.get('title','Untitled'),
author=row.get('author'),
isbn=str(row.get('isbn')) if not pd.isna(row.get('isbn')) else None,
copies_total=int(row.get('copies',1)),
copies_available=int(row.get('copies',1)),
category_id=cat.id,
description=row.get('description')
)
session.add(book)
session.commit()




def books_to_excel(books):
rows = []
for b in books:
rows.append({
'title': b.title,
'author': b.author,
'isbn': b.isbn,
'category': b.category.name if b.category else None,
'copies_total': b.copies_total,
'copies_available': b.copies_available,
'description': b.description,
})
df = pd.DataFrame(rows)
buf = BytesIO()
df.to_excel(buf, index=False)
buf.seek(0)
return buf