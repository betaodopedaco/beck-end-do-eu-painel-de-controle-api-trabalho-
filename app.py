# API principal do backend (FastAPI)
import os
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
from datetime import datetime, timedelta

from database import criar_banco, get_session
import crud
from models import Cliente

ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN', 'token-demo')

app = FastAPI(title='MAGNATUNS - Backend')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
def startup_event():
    criar_banco()

# dependência simples de autenticação admin
def autenticar_admin(x_admin_token: str = Header(None)):
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail='Token admin inválido')
    return True

class ClienteCreate(BaseModel):
    nome: str
    email: str
    telefone: str = None
    site: str = None
    repo: str = None
    tokens_mes: int = 100000

class AjusteTokens(BaseModel):
    tokens_mes: int

@app.get('/admin/metrics/overview')
def overview(admin=Depends(autenticar_admin)):
    with get_session() as s:
        clientes = crud.listar_clientes(s)
        total_clients = len(clientes)
        mrr = sum(1 for c in clientes if c.status == 'pago') * 80
        total_tokens_used = sum((c.tokens_usados or 0) for c in clientes)
        return {
            'total_clients': total_clients,
            'mrr': mrr,
            'total_tokens_used': total_tokens_used
        }

@app.get('/admin/clients', response_model=List[Cliente])
def admin_list_clients(admin=Depends(autenticar_admin)):
    with get_session() as s:
        return crud.listar_clientes(s)

@app.post('/admin/clients', response_model=Cliente)
def admin_create_client(payload: ClienteCreate, admin=Depends(autenticar_admin)):
    with get_session() as s:
        data = payload.dict()
        data['proxima_cobranca'] = datetime.utcnow() + timedelta(days=7)
        c = crud.criar_cliente(s, data)
        return c

@app.get('/admin/clients/{cliente_id}', response_model=Cliente)
def admin_get_client(cliente_id: int, admin=Depends(autenticar_admin)):
    with get_session() as s:
        c = crud.obter_cliente(s, cliente_id)
        if not c:
            raise HTTPException(status_code=404, detail='Cliente não encontrado')
        return c

@app.post('/admin/clients/{cliente_id}/swap')
def admin_swap(cliente_id:int, admin=Depends(autenticar_admin)):
    with get_session() as s:
        c = crud.obter_cliente(s, cliente_id)
        if not c:
            raise HTTPException(status_code=404, detail='Cliente não encontrado')
        c.status = 'pago'
        if not c.proxima_cobranca:
            c.proxima_cobranca = datetime.utcnow() + timedelta(days=30)
        crud.atualizar_cliente(s, c)
        return {'ok': True, 'message': 'Cliente ativado como pago'}

@app.post('/admin/clients/{cliente_id}/adjust')
def admin_adjust(cliente_id:int, payload: AjusteTokens, admin=Depends(autenticar_admin)):
    with get_session() as s:
        c = crud.obter_cliente(s, cliente_id)
        if not c:
            raise HTTPException(status_code=404, detail='Cliente não encontrado')
        c.tokens_mes = payload.tokens_mes
        crud.atualizar_cliente(s, c)
        return {'ok': True, 'tokens_mes': c.tokens_mes}

@app.post('/log/request')
def log_request(cliente_id: int, tokens_in:int=0, tokens_out:int=0):
    with get_session() as s:
        rl = crud.registrar_request(s, cliente_id, tokens_in, tokens_out)
        return {'ok': True, 'id': rl.id}
