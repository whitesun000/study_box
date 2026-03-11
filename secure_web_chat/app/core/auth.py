from fastapi import APIRouter, Form, responses, status
from app.core.database import get_db_connection

router = APIRouter()

@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 【重要】「?」によるバインド
    # これにより ' OR '1'='1 などの攻撃が無効化されます
    query = "SELECT * FROM users WHERE username = ? AND password = ? "
    cursor.execute(query, (username, password))

    user = cursor.fetchone()
    conn.close()

    if user:
        return responses.RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return {"status": "fail", "message": "ユーザー名かパスワードが違います。"}