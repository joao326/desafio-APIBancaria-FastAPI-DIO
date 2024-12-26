import databases
import sqlalchemy as sa

from src.config import settings

# cria uma instância de conexão ao banco de dados com base na URL configurada
database = databases.Database(settings.database_url)

# instancia o objeto metadata para mapear os esquemas do banco de dados
metadata = sa.MetaData()

# verifica se o ambiente é de produção para configurar o motor de conexão corretamente
if settings.environment == "production":
    # em produção, cria o motor de conexão sem argumentos adicionais
    engine = sa.create_engine(settings.database_url)
else:
    # em outros ambientes, desabilita a verificação de thread para SQLite
    engine = sa.create_engine(settings.database_url, connect_args={"check_same_thread": False})
