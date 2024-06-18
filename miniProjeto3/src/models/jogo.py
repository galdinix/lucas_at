from sqlalchemy import Column, String
from conexaoBd.database import Base

class Jogo(Base):
    __tablename__ = "jogos"

    tipo = Column(String, primary_key=True, index=True)
    jogo = Column(String, primary_key=True, index=True)
