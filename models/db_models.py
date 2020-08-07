from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Sequence
from sqlalchemy.orm import relationship
from models.base import base



class Produto(base):
    __tablename__ = 'produto'
    produto_id = Column(Integer, Sequence('produto_id_auto_incremento', start=1), primary_key=True)
    nome = Column(String)
    descrição = Column(String)
    preco = Column(String)