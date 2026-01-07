from fastapi import APIRouter, HTTPException, status
from schemas import LoginRequest, UserCreate, UserResponse
from database import get_user, create_user, list_users, update_user, delete_user
from security import hash_password, verify_password
from schemas import LoginRequest
from main import * 

router = APIRouter()


#================ LOGIN ===================
@router.post("/login")
def login(dados: LoginRequest):
    usuario = get_user(dados.user)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

    if usuario["user"] == "admin":
        if verify_password(dados.senha, usuario["senha"]):
            return {"user": dados.user, "status": "logado como admin"}
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha incorreta para admin")

    if verify_password(dados.senha, usuario["senha"]):
        return {"user": dados.user, "status": "logado"}
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Senha incorreta")

#================ CREATE ===================
@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user_route(dados: UserCreate):
    senha_hash = hash_password(dados.senha)
    if not create_user(dados.user, senha_hash):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Usuário já existe")
    return {"message": "Usuário criado", "user": dados.user}

#================ LIST ===================
@router.get("/users", response_model=list[UserResponse])
def list_users_route():
    return list_users()

#================ GET USER ===================
@router.get("/users/{username}", response_model=UserResponse)
def get_user_route(username: str):
    usuario = get_user(username)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return {"user": usuario["user"]}

#================ UPDATE USER ===================
@router.put("/users/{username}")
def update_user_route(username: str, dados: UserCreate):
    usuario = get_user(username)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    senha_hash = hash_password(dados.senha)
    if not update_user(username, dados.user, senha_hash):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Não foi possível atualizar o usuário")
    return {"message": "Usuário atualizado", "user": dados.user}

#================ DELETE USER ===================
@router.delete("/users/{username}")
def delete_user_route(username: str, senha: str):
    success = delete_user(username, senha)
    if not success:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado ou senha incorreta")
    return {"message": "Usuário deletado", "user": username}

