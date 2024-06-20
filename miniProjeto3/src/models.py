from sqlalchemy import Column, String, Integer
from database import*

class Jogo(Base):
    __tablename__ = "jogos"

    id_jogo = Column(Integer, primary_key=True)
    tipo = Column(String)
    jogo = Column(String)
