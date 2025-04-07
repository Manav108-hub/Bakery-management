from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import DeclarativeBase  # Add this import
from src.config import settings
from urllib.parse import quote_plus

# Define the Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# URL-encode the password
encoded_password = quote_plus(settings.DB_PASSWORD)
DATABASE_URL = f"postgresql+psycopg2://{settings.DB_USER}:{encoded_password}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
print(f"Database URL: {DATABASE_URL}")  # For debugging

# Create a synchronous engine
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10
)

# Create a session factory for synchronous sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to provide a synchronous database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_db_connection():
    # Synchronous function to check the database connection
    with engine.connect() as conn:
        pass  # If this succeeds, the connection is established