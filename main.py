from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_routes, user_routes, admin_routes, book_routes
from app.database import Base, engine
from app.config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management System",
    version="1.0.0",
    description="API for managing library operations, users, and books."
)

# CORS setup
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(admin_routes.router, prefix="/admin", tags=["Admin"])
app.include_router(book_routes.router, prefix="/books", tags=["Books"])

@app.get("/")
def home():
    return {"message": "Welcome to the Library Management System API"}

