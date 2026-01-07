from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi import FastAPI, Request, Form
from schemas import LoginRequest, UserCreate
from users import router as users_router, create_user_route, login, list_users_route, delete_user_route

app = FastAPI()
app.include_router(users_router)
templates = Jinja2Templates(directory="templates")

# Página inicial
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "usuarios": list_users_route()})

# Login via formulário
@app.post("/login_web")
def login_web(request: Request, user: str = Form(...), senha: str = Form(...)):
    login_data = LoginRequest(user=user, senha=senha)
    result = login(login_data)
    return templates.TemplateResponse("index.html", {"request": request, "usuarios": list_users_route()})

# Criar usuário via formulário
@app.post("/create_user_web")
def create_user_web(request: Request, user: str = Form(...), senha: str = Form(...)):
    user_data = UserCreate(user=user, senha=senha)
    create_user_route(user_data)  # usa a função do users.py
    return templates.TemplateResponse("index.html", {"request": request, "usuarios": list_users_route()})

# Deletar usuário via formulário
@app.post("/delete_user_web")
def delete_user_web(request: Request, user: str = Form(...), senha: str = Form(...)):
    success = delete_user_route(user, senha)
    return templates.TemplateResponse("index.html", {"request": request, "usuarios": list_users_route()})


# ================= Favicon and Leyley ===================
@app.get("/favicon.ico")
@app.get("/leyley")
def leyley():
    return FileResponse("leyley.png")
#só fixação mesmo

