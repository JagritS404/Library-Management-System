from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


class User(SQLModel, table=True):
id: Optional[int] = Field(default=None, primary_key=True)
email: str = Field(index=True, nullable=False)
name: Optional[str]
hashed_password: Optional[str]
is_admin: bool = Field(default=False)
created_at: datetime = Field(default_factory=datetime.utcnow)
borrowed: List["Borrow"] = Relationship(back_populates="user")


class Category(SQLModel, table=True):
id: Optional[int] = Field(default=None, primary_key=True)
name: str
description: Optional[str] = None
books: List["Book"] = Relationship(back_populates="category")


class Book(SQLModel, table=True):
id: Optional[int] = Field(default=None, primary_key=True)
title: str
author: Optional[str]
isbn: Optional[str] = Field(index=True)
copies_total: int = Field(default=1)
copies_available: int = Field(default=1)
category_id: Optional[int] = Field(default=None, foreign_key="category.id")
category: Optional[Category] = Relationship(back_populates="books")
description: Optional[str]
created_at: datetime = Field(default_factory=datetime.utcnow)
borrows: List["Borrow"] = Relationship(back_populates="book")


class Borrow(SQLModel, table=True):
id: Optional[int] = Field(default=None, primary_key=True)
user_id: int = Field(foreign_key="user.id")
book_id: int = Field(foreign_key="book.id")
issued_at: datetime = Field(default_factory=datetime.utcnow)
due_date: Optional[datetime]
returned_at: Optional[datetime] = None


user: Optional[User] = Relationship(back_populates="borrowed")
book: Optional[Book] = Relationship(back_populates="borrows")