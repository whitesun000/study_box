import os
from pathlib import Path
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Secure Web Chat Ecosystem"

    # サーバー設定 (.env から取得、なければデフォルト値)
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", 8000))

    # ディレクトリパスの設定
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    STATIC_DIR: str = str(BASE_DIR / "app" / "static")
    TEMPLATE_DIR: str = str(BASE_DIR / "app" / "templates")
    DB_PATH: str = str(BASE_DIR / "data" / "chat_app.sqlite3")

    SESSION_COOKIE_NAME = "session_user"

settings = Settings()