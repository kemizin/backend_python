from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import logging

from .routes.users import router as users_router
from .database import list_users

app = FastAPI()

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    logging.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# inclui TODAS as rotas da pasta routes
app.include_router(users_router)

templates = Jinja2Templates(directory="inicio_backend/templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    usuarios = list_users()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "usuarios": usuarios}
    )

@app.post("/login_web")
def login_web(
    user: str = Form(...),
    senha: str = Form(...)
):
    from .database import get_user
    from .security import verify_password

    usuario = get_user(user)
    if not usuario or not verify_password(senha, usuario["senha"]):
        return RedirectResponse("/", status_code=303)

    return RedirectResponse("/", status_code=303)

@app.post("/create_user_web")
def create_user_web(
    user: str = Form(...),
    senha: str = Form(...)
):
    from .database import create_user
    from .security import hash_password

    create_user(user, hash_password(senha))
    return RedirectResponse("/", status_code=303)

@app.post("/delete_user_web")
def delete_user_web(
    user: str = Form(...),
    senha: str = Form(...)
):
    from .database import delete_user

    delete_user(user, senha)
    return RedirectResponse("/", status_code=303)


@app.get("/leyley")
def leyley():
    return FileResponse("leyley.png")
