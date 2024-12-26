import time
from typing import Annotated
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

# define uma secret key para assinar tokens JWT e algoritmo de criptografia
SECRET = "my-secret"
ALGORITHM = "HS256"

# define o modelo de dados para o payload do token de acesso
class AccessToken(BaseModel):
    iss: str  # emissor do token
    sub: int  # identificador do usuário
    aud: str  # público alvo do token
    exp: float  # timestamp de expiração do token
    iat: float  # timestamp de criação do token
    nbf: float  # token não será válido antes deste timestamp
    jti: str  # identificador único do token

# define o modelo de dados para o token JWT completo
class JWTToken(BaseModel):
    access_token: AccessToken

# função para criar e assinar um token JWT para o usuário
def sign_jwt(user_id: int) -> JWTToken:
    now = time.time()  # obtém o timestamp atual
    payload = {
        "iss": "desafio-bank.com.br",  # emissor fixo do token
        "sub": user_id,  # id do usuário
        "aud": "desafio-bank",  # público alvo fixo
        "exp": now + (60 * 30),  # tempo de expiração (30 minutos)
        "iat": now,  # data de emissão
        "nbf": now,  # não pode ser usado antes deste momento
        "jti": uuid4().hex,  # id único do token
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)  # assina o token
    return {"access_token": token}  # retorna o token como um dicionário

# função para decodificar e validar um token JWT
async def decode_jwt(token: str) -> JWTToken | None:
    try:
        # decodifica o token JWT e valida o público e o algoritmo
        decoded_token = jwt.decode(token, SECRET, audience="desafio-bank", algorithms=[ALGORITHM])
        # valida o payload do token como um modelo JWTToken
        _token = JWTToken.model_validate({"access_token": decoded_token})
        # verifica se o token ainda é válido pelo timestamp de expiração
        return _token if _token.access_token.exp >= time.time() else None
    except Exception:
        # retorna None em caso de falha na validação ou decodificação
        return None

# classe para autenticação baseada em JWT
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        # inicializa a classe base com a opção de erro automático
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> JWTToken:
        # obtém o cabeçalho de autorização da requisição
        authorization = request.headers.get("Authorization", "")
        scheme, _, credentials = authorization.partition(" ")

        if credentials:
            if not scheme == "Bearer":
                # verifica se o esquema é "Bearer"
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme.",
                )

            payload = await decode_jwt(credentials)
            if not payload:
                # retorna erro se o token for inválido ou expirado
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired token.",
                )
            return payload  # retorna o token decodificado
        else:
            # retorna erro se não houver credenciais
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization code.",
            )

# função para obter o usuário atual a partir do token JWT
async def get_current_user(
    token: Annotated[JWTToken, Depends(JWTBearer())],
) -> dict[str, int]:
    # retorna o id do usuário extraído do token JWT
    return {"user_id": token.access_token.sub}

# função decoradora para verificar se o login é necessário
def login_required(current_user: Annotated[dict[str, int], Depends(get_current_user)]):
    if not current_user:
        # retorna erro se o usuário não estiver autenticado
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return current_user  # retorna o usuário autenticado
