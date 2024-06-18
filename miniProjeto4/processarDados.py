import pandas as pd
from sqlalchemy import create_engine, inspect
import pathlib

# Ajuste o caminho do banco de dados
base_dir = pathlib.Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{base_dir / 'miniProjeto3' / 'data' / 'jogos.db'}"
print(f"Database URL: {DATABASE_URL}")

# Configurar o engine do SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Testar a conexão e consultar dados
def main():
    try:
        # Usar o inspector para verificar se a tabela existe
        inspector = inspect(engine)
        if not inspector.has_table('jogos'):
            print("Tabela 'jogos' não encontrada no banco de dados.")
        else:
            # Consultar todos os dados da tabela "jogos"
            query = "SELECT * FROM jogos"
            df = pd.read_sql(query, engine)
            print("Dados consultados:")
            print(df)
            return df
    except Exception as e:
        print(f"Erro ao consultar dados: {e}")
        
