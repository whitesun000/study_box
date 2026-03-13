from fastapi import APIRouter, Form, responses, status
from app.core.database import get_db_connection
from app.core.security import get_password_hash, verify_password

router = APIRouter()

# グローバル変数でモードを管理（初期値は安全モード）
is_vulnerable_mode = False

@router.post("/toggle_security")
async def toggle_security():
    global is_vulnerable_mode
    is_vulnerable_mode = not is_vulnerable_mode
    current_mode = "VULNERABLE" if is_vulnerable_mode else "SAFE"
    return {"status": current_mode}


@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

         # 1. データベースにユーザーを探しに行く
        if is_vulnerable_mode:
            # ⚠️ 脆弱なコード：文字列をそのまま合体させる
            # これにより ' OR '1'='1 などの SQLインジェクションが成功します。
            query = f"SELECT password FROM users WHERE username = '{username}'"
            cursor.execute(query)
        else:
            # ✅ 安全なコード：プレースホルダ(?)を使う
            query = "SELECT password FROM users WHERE username = ?"    
            cursor.execute(query, (username,))

        user = cursor.fetchone()

        # 2. 見つかったユーザーに対して認証を行う
        if user:
            # SQLインジェクションの兆候があるかチェック
            is_sql_injection = "'" in username or "OR" in username.upper()

            if is_vulnerable_mode:
                # ⚠️ 脆弱モードならパスワード不一致でも入れるが...
                auth_success = True
                # 攻撃コードを使った場合、または脆弱モードを利用した場合は「Hacker」
                if is_sql_injection:
                    user_display_name = "Hacker"
                else:
                    user_display_name = username
            else:
                # ✅ 安全モードなら厳格にチェック
                auth_success = verify_password(password, user[0])
                user_display_name = username
            
            if auth_success:
                # ログイン成功時の処理
                res = responses.RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
                user_display_name = "Hacker" if is_vulnerable_mode else username
                res.set_cookie(key="session_user", value=user_display_name, httponly=True)
                return res
    except Exception as e:
        print(f"Login Error: {e}")
        return responses.RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    finally:
        conn.close()
     
    # 3. 認証失敗時、またはユーザーが見つからない場合
    return responses.RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    

@router.get("/security_status")
async def get_security_status():
    global is_vulnerable_mode
    return {"status": "VULNERABLE" if is_vulnerable_mode else "SAFE"}


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

