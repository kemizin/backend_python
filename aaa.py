from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from fastapi import Form
from fastapi.responses import RedirectResponse
from .schemas import UserCreate
from .database import list_users
from .routes.users import create_user_route
from fastapi import Form
from fastapi.responses import RedirectResponse
from .schemas import LoginRequest
from .routes.users import login



from .routes.users import router as users_router

app = FastAPI()
app.include_router(users_router)

templates = Jinja2Templates(directory="inicio_backend/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    usuarios = list_users()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "usuarios": usuarios}
    )

@app.post("/create_user_web")
def create_user_web(user: str = Form(...), senha: str = Form(...)):
    create_user_route(UserCreate(user=user, senha=senha))
    return RedirectResponse("/", status_code=303)

@app.post("/login_web")
def login_web(user: str = Form(...), senha: str = Form(...)):
    login(LoginRequest(user=user, senha=senha))
    return RedirectResponse("/", status_code=303)

from .routes.users import delete_user_route

@app.post("/delete_user_web")
def delete_user_web(user: str = Form(...), senha: str = Form(...)):
    delete_user_route(user, senha)
    return RedirectResponse("/", status_code=303)



@app.get("/favicon.ico")
@app.get("/leyley")
def leyley():
    return FileResponse("inicio_backend/leyley.png")
