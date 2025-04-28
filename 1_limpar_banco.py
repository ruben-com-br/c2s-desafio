from sqlalchemy import create_engine
from db.base import Base

def limpar_banco():
    db_path = "automoveis.db"
    engine = create_engine(f"sqlite:///{db_path}")
    
    print("⚠️ ATENÇÃO: Isso irá apagar TODOS os dados do banco!")
    confirmacao = input("Tem certeza que deseja continuar? (s/n): ")
    
    if confirmacao.lower() == 's':
        Base.metadata.drop_all(engine)
        print("✅ Banco de dados limpo com sucesso!")
    else:
        print("Operação cancelada.")

if __name__ == "__main__":
    limpar_banco()