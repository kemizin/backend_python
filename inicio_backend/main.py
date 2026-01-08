from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse

from schemas import LoginRequest, UserCreate
from users import (
    router as users_router,
    list_users,
    create_user,
    login_user,
    delete_user
)

app = FastAPI()
app.include_router(users_router)

templates = Jinja2Templates(directory="templates")

# ======================
# Página inicial
# ======================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "usuarios": list_users()
        }
    )

# ======================
# Login via formulário
# ======================
@app.post("/login_web")
def login_web(user: str = Form(...), senha: str = Form(...)):
    login_user(LoginRequest(user=user, senha=senha))
    return RedirectResponse("/", status_code=303)

# ======================
# Criar usuário
# ======================
@app.post("/create_user_web")
def create_user_web(user: str = Form(...), senha: str = Form(...)):
    create_user(UserCreate(user=user, senha=senha))
    return RedirectResponse("/", status_code=303)

# ======================
# Deletar usuário
# ======================
@app.post("/delete_user_web")
def delete_user_web(user: str = Form(...), senha: str = Form(...)):
    delete_user(user, senha)
    return RedirectResponse("/", status_code=303)

# ======================
# Favicon / imagem
# ======================
@app.get("/favicon.ico")
@app.get("/leyley")
def leyley():
    return FileResponse("leyley.png")
