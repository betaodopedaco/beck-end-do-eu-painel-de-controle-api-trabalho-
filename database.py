# Conexão com o banco e gerador de sessão.
from sqlmodel import SQLModel, create_engine, Session
import os

# Se DATABASE_URL não for fornecido, usamos um sqlite local para desenvolvimento.
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    DATABASE_URL = 'sqlite:///./magnatuns.db'

engine = create_engine(DATABASE_URL, echo=False)

def criar_banco():
    SQLModel.metadata.create_all(engine)

from contextlib import contextmanager
@contextmanager
def get_session():
    with Session(engine) as session:
        yield session
