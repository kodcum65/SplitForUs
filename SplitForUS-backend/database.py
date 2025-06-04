import json
from pathlib import Path

DATA_FILE = Path("data/tables.json")

def load_data():
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
# ─── SQLAlchemy Ayarları ──────────────────────────────────────────


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Veritabanı URL’iniz; SQLite kullanıyorsanız:
SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"

# Engine ve SessionLocal tanımı
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite için
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base sınıfı; modellerinizin miras aldığı sınıf
Base = declarative_base()

# Dependency: her istek için DB oturumu açıp kapatacak
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
