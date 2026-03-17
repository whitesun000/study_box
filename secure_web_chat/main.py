import uvicorn

from fastapi import FastAPI, Request, responses
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core import websocket_handler, auth, admin

from app.core.database import init_db




# 起動時にDBを準備
init_db()

app = FastAPI(title=settings.PROJECT_NAME)

# 設定クラスからパスを取得
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")
templates = Jinja2Templates(directory=settings.TEMPLATE_DIR)

# WebSocket用のルーター登録
app.include_router(websocket_handler.router)

# 認証用のルーター登録 (プレフィックス "/auth" を付ける)
app.include_router(auth.router, prefix="/auth")

# 管理者用のルーター登録
app.include_router(admin.router)

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    user = request.cookies.get("session_user")
    if not user:
        return responses.RedirectResponse(url="/login")
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)