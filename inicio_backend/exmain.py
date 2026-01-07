from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field
from fastapi import status
from fastapi import HTTPException, status
from database import fake_users_db

app = FastAPI()

@app.get("/")
def home():
    return HTMLResponse("""
    <html>
        <head>
            <link rel="icon" href="/favicon.ico">
        </head>
        <body>
            <h1>API ON 🔥</h1>
        </body>
    </html>
    """)

@app.get("/favicon.ico")
def favicon():
    return FileResponse("favicon.ico")

@app.get("/leyley")
def leyley():
    return FileResponse("leyley.png")

class LoginRequest(BaseModel):
    user: str
    senha: str = Field(min_length=6)   




@app.post("/login")
def login(dados: LoginRequest):
    for usuario in fake_users_db:
        if usuario["user"] == dados.user and usuario["user"] == "admin":
            if usuario["senha"] == dados.senha:
                return {"user": dados.user, "status": "logado como admin"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Senha incorreta para admin"
                )
        if usuario["user"] == dados.user:
            if usuario["senha"] == dados.senha:
                return {"user": dados.user, "status": "logado"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Senha incorreta"
                )
            

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuário não encontrado"
    )#isso é um tratamento de erro, vc apelida um erro com uma mensagem personalizada


#============================
@app.post("/login", status_code=status.HTTP_200_OK)
def login(dados: LoginRequest):
    return {"user": dados.user, "status": "logado"}
#============================




class UserCreate(BaseModel):
    user: str = Field(min_length=3, max_length=50)
    senha: str = Field(min_length=6)

def user_exists(username: str):
    for usuario in fake_users_db:
        if usuario["user"] == username:
            return True
    return False

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(dados: UserCreate):
    if user_exists(dados.user):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Usuário já existe"
        )

    novo_usuario = {
        "user": dados.user,
        "senha": dados.senha
    }

    fake_users_db.append(novo_usuario)

    return {
        "message": "Usuário criado com sucesso",
        "user": dados.user
    }

@app.get("/users")
def list_users():
    usuarios_publicos = []

    for usuario in fake_users_db:
        usuarios_publicos.append({
            "user": usuario["user"]
        })

    return usuarios_publicos
