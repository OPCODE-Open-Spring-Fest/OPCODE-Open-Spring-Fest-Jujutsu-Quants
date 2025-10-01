# app/database/database.py - Modified for LOCAL PostgreSQL connection
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.database.models import Base # Ensure this import is correct based on your models.py
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables. Crucial if this file is imported first.
load_dotenv()

# --- Database Configuration for LOCAL PostgreSQL ---
# These should be defined in your .env file in the project root
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST", "localhost") # Default to localhost if not set
DB_PORT = os.getenv("DB_PORT", "5432")     # Default to standard PostgreSQL port

# Check for critical environment variables
if not all([DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT]):
    raise ValueError(
        "Missing one or more crucial database environment variables "
        "(DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT) "
        "for local PostgreSQL connection."
    )


SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?host={DB_HOST}"
)



# Create the SQLAlchemy engine for LOCAL PostgreSQL
# echo=True is helpful for debugging, set to False for production
print(f"🐘 Connecting to LOCAL PostgreSQL at {DB_HOST}:{DB_PORT} with database {DB_NAME}...")
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False # Set to True to see all generated SQL queries
)
print("✅ Local PostgreSQL engine created")

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all tables in the database."""
    try:
        # Base.metadata.create_all requires 'Base' to be imported or defined.
        # Assuming `app.database.models.Base` is where it's defined.
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully (or already exist)")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise

def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database on module import
create_tables()

# The `connector` variable and `close_connections` function (related to Cloud SQL Connector)
# are no longer needed for local PostgreSQL, so they are removed from this version.