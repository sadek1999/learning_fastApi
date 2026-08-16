from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"

# 2. Create the SQLAlchemy engine
# connect_args={"check_same_thread": False} is required ONLY for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# 3. Create a SessionLocal class
# Each request will get its own database session from this factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create a Base class
# Your ORM models (app/models.py) will inherit from this Base class
Base = declarative_base()


# 5. Dependency to get DB session per request
def get_db():
    """
    FastAPI dependency that provides a database session to endpoints
    and automatically closes it when the request is complete.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()