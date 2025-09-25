# Modelos de dados (SQLModel)
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Plano(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    preco: float
    tokens_mes: int

class Cliente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str
    telefone: Optional[str] = None
    site: Optional[str] = None
    repo: Optional[str] = None
    status: str = 'demo'  # demo, pago, suspenso, cancelado
    tokens_mes: int = 100000
    tokens_usados: int = 0
    proxima_cobranca: Optional[datetime] = None
    criado_em: datetime = Field(default_factory=datetime.utcnow)

class ApiKey(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_id: Optional[int] = Field(default=None)
    provider: str
    chave: str
    modelo: Optional[str] = None
    status: str = 'ativa'  # ativa, expirada, bloqueada
    validade: Optional[datetime] = None

class RequestLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_id: Optional[int] = Field(default=None)
    tokens_input: int = 0
    tokens_output: int = 0
    latency_ms: Optional[int] = None
    status_code: Optional[int] = None
    criado_em: datetime = Field(default_factory=datetime.utcnow)

class Invoice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_id: Optional[int] = Field(default=None)
    valor: float
    status: str = 'pending'  # pending, paid, failed
    criado_em: datetime = Field(default_factory=datetime.utcnow)
