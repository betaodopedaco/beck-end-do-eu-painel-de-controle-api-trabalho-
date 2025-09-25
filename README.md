# MAGNATUNS Backend (FastAPI)

Projeto backend mínimo para o MVP do painel MAGNATUNS.

## Como usar (local)
1. Copie `.env.example` para `.env` e preencha `DATABASE_URL` e `ADMIN_TOKEN`.
2. Instale dependências: `pip install -r requirements.txt`
3. Rode localmente: `uvicorn app:app --reload --host 0.0.0.0 --port 8000`

## Endpoints principais (Admin)
- `GET /admin/clients` — lista clientes (header `x-admin-token` com o token)
- `POST /admin/clients` — cria cliente (JSON body)
- `GET /admin/clients/{id}` — obtém cliente
- `POST /admin/clients/{id}/swap` — ativa versão paga (swap demo->pago)
- `POST /admin/clients/{id}/adjust` — ajustar limite tokens (json: {"tokens_mes": 200000})
- `GET /admin/metrics/overview` — retorna KPIs simples
- `POST /log/request` — registrar uso de tokens (webhook do proxy/endpoint)

Esse repositório é um esqueleto para você rodar no Render. Posso completar integrações (pagamentos, compra automática de API) se quiser.
