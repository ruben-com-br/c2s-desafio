import uvicorn
from fastapi import FastAPI, Query
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.car import Car
from db.base import Base
from typing import List, Optional

app = FastAPI()

# Conexão com o banco de dados
db_path = "automoveis.db"
engine = create_engine(f"sqlite:///{db_path}")
Session = sessionmaker(bind=engine)

@app.get("/buscar_carros")
def buscar_carros(
    marca: Optional[str] = Query(None),
    modelo: Optional[str] = Query(None),
    ano: Optional[int] = Query(None),
    tipo_combustivel: Optional[str] = Query(None),
    preco_min: Optional[float] = Query(None),
    preco_max: Optional[float] = Query(None)
) -> List[dict]:
    session = Session()
    query = session.query(Car)

    # Aplicando filtros
    if marca:
        query = query.filter(Car.marca.ilike(f"%{marca}%"))
    if modelo:
        query = query.filter(Car.modelo.ilike(f"%{modelo}%"))
    if ano:
        query = query.filter(Car.ano == ano)
    if tipo_combustivel:
        query = query.filter(Car.tipo_combustivel.ilike(f"%{tipo_combustivel}%"))
    if preco_min:
        query = query.filter(Car.preco >= preco_min)
    if preco_max:
        query = query.filter(Car.preco <= preco_max)

    carros = query.all()

    return [
        {
            "marca": carro.marca,
            "modelo": carro.modelo,
            "ano": carro.ano,
            "cor": carro.cor,
            "quilometragem": carro.quilometragem,
            "preco": carro.preco,
            "tipo_combustivel": carro.tipo_combustivel
        }
        for carro in carros
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)