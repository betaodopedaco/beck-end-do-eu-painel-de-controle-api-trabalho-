# Operações básicas de banco
from sqlmodel import select
from models import Cliente, ApiKey, RequestLog, Invoice, Plano
from database import get_session
from typing import Optional

def listar_clientes(session):
    return session.exec(select(Cliente)).all()

def obter_cliente(session, cliente_id: int) -> Optional[Cliente]:
    return session.get(Cliente, cliente_id)

def criar_cliente(session, dados: dict) -> Cliente:
    c = Cliente(**dados)
    session.add(c)
    session.commit()
    session.refresh(c)
    return c

def atualizar_cliente(session, cliente: Cliente):
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente

def registrar_request(session, cliente_id:int, in_tokens:int, out_tokens:int, status_code:int=None, latency_ms:int=None):
    rl = RequestLog(cliente_id=cliente_id, tokens_input=in_tokens, tokens_output=out_tokens, status_code=status_code, latency_ms=latency_ms)
    session.add(rl)
    cli = session.get(Cliente, cliente_id)
    if cli:
        cli.tokens_usados = (cli.tokens_usados or 0) + in_tokens + out_tokens
        session.add(cli)
    session.commit()
    session.refresh(rl)
    return rl
