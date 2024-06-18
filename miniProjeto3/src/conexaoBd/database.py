from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pathlib

base_dir = pathlib.Path(__file__).resolve().parent.parent.parent.parent
DATABASE_URL = f"sqlite:///{base_dir / 'miniProjeto3' / 'data' / 'jogos.db'}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def oi():
    print('oi')