from fastapi import APIRouter, Form, responses, status
from app.core.database import get_db_connection
from app.core.security import get_password_hash, verify_password

router = APIRouter()

@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 【重要】「?」によるバインド
    # これにより ' OR '1'='1 などの攻撃が無効化されます
    query = "SELECT password FROM users WHERE username = ?"    
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    conn.close()

    if user and verify_password(password, user[0]):
        res = responses.RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        res.set_cookie(key="session_user", value=username, httponly=True)
        return res
    else:
        return {"status": "fail", "message": "ユーザー名かパスワードが違います。"}

@router.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 重複チェック：同じ名前のユーザーがいないか確認
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return {"status": "fail", "message": "そのユーザー名は既に使用されています。"}
        
        hashed_password = get_password_hash(password)   # パスワードをハッシュ化
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()

        # 登録できたらログイン画面へ飛ばす
        return responses.RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()

@router.get("/logout")
async def logout():
    response = responses.RedirectResponse(url="/login")
    response.delete_cookie("session_user")
    return response