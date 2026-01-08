from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .routes.users import router as users_router
from .database import list_users

app = FastAPI()

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


@app.get("/leyley")
def leyley():
    return FileResponse("leyley.png")
