from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.controllers import account, auth, transaction
from src.database import database
from src.exceptions import AccountNotFoundError, BusinessError

# define um gerenciador de contexto assíncrono para gerenciar o ciclo de vida do banco de dados
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()  # conecta ao banco de dados no início do ciclo de vida
    yield  # permite que o FastAPI continue o fluxo de execução
    await database.disconnect()  # desconecta do banco de dados no final do ciclo de vida

# define metadados para categorizar endpoints na documentação OpenAPI
tags_metadata = [
    {
        "name": "auth",
        "description": "Operations for authentication.",  # descrição das operações relacionadas à autenticação
    },
    {
        "name": "account",
        "description": "Operations to maintain accounts.",  # descrição das operações de gerenciamento de contas
    },
    {
        "name": "transaction",
        "description": "Operations to maintain transactions.",  # descrição das operações de transações
    },
]

# cria a aplicação FastAPI com configurações e metadados
app = FastAPI(
    title="Transactions API",  # título da aplicação
    version="1.0.0",  # versão da aplicação
    summary="Microservice to maintain withdrawal and deposit operations from current accounts.",  # resumo do serviço
    description="""
Transactions API is the microservice for recording current account transactions. 💸💰

## Account

* **Create accounts**.
* **List accounts**.
* **List account transactions by ID**.

## Transaction

* **Create transactions**.
""",  # descrição detalhada exibida na documentação OpenAPI
    openapi_tags=tags_metadata,  # tags para categorização de endpoints
    redoc_url=None,  # desabilita a interface Redoc
    lifespan=lifespan,  # gerenciador de ciclo de vida da aplicação
)

# adiciona middleware CORS para permitir comunicação com outros domínios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # permite requisições de qualquer origem
    allow_credentials=True,  # permite envio de cookies
    allow_methods=["*"],  # permite todos os métodos HTTP
    allow_headers=["*"],  # permite todos os cabeçalhos HTTP
)

# inclui os roteadores para autenticação, contas e transações
app.include_router(auth.router, tags=["auth"])  # rota para operações de autenticação
app.include_router(account.router, tags=["account"])  # rota para operações de conta
app.include_router(transaction.router, tags=["transaction"])  # rota para operações de transação

# define manipulador de exceção para erros de conta não encontrada
@app.exception_handler(AccountNotFoundError)
async def account_not_found_error_handler(request: Request, exc: AccountNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Account not found."})

# define manipulador de exceção para erros de negócio
@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, exc: BusinessError):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})
