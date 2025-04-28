from db.base import Base  # Importando a variável Base do arquivo base.py
from sqlalchemy import Column, Integer, String, Float

class Car(Base):
    __tablename__ = 'carros'

    id = Column(Integer, primary_key=True, autoincrement=True)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)
    motorizacao = Column(String)
    tipo_combustivel = Column(String)
    cor = Column(String)
    quilometragem = Column(Integer)
    numero_portas = Column(Integer)
    transmissao = Column(String)
    placa = Column(String)
    preco = Column(Float)

