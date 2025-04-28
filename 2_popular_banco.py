from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.car import Car
from db.base import Base
from faker import Faker

def popular_banco(qtd=100):
    db_path = "automoveis.db"
    engine = create_engine(f"sqlite:///{db_path}")
    Session = sessionmaker(bind=engine)
    session = Session()
    fake = Faker()

    # Criar tabelas se não existirem
    Base.metadata.create_all(engine)

    for _ in range(qtd):
        carro = Car(
            marca=fake.company(),
            modelo=fake.word(),
            ano=fake.random_int(min=1970, max=2023),
            motorizacao=fake.random_element(elements=("1.0", "1.6", "2.0", "2.4", "3.0")),
            tipo_combustivel=fake.random_element(elements=("Gasolina", "Álcool", "Flex", "Diesel", "Elétrico")),
            cor=fake.color_name(),
            quilometragem=fake.random_number(digits=5),
            numero_portas=fake.random_int(min=2, max=5),
            transmissao=fake.random_element(elements=("Manual", "Automático", "CVT", "Semi-automático")),
            placa=fake.license_plate(),
            preco=fake.random_number(digits=5)
        )
        session.add(carro)

    session.commit()
    print(f"{qtd} carros adicionados ao banco!")

if __name__ == "__main__":
    popular_banco(100)