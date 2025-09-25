Instruções rápidas para deploy no Render:

1. Crie um repositório no GitHub e envie este projeto.
2. No Render, crie um novo Web Service apontando para o repositório.
3. Configure as variáveis de ambiente (DATABASE_URL, ADMIN_TOKEN, SECRET_KEY).
4. Use o comando de start: `uvicorn app:app --host 0.0.0.0 --port $PORT`.
