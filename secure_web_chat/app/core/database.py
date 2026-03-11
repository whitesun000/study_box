import os
import sqlite3
from app.core.config import settings

def get_db_connection():
    # settings.DB_PATH から親フォルダのパスを取得
    db_file = settings.DB_PATH
    db_dir = os.path.dirname(db_file)

    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        print(f"Directory '{db_dir}' created.")

    # .env や config で設定したパスを使ってDBに接続
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row  # カラム名でデータを取り出せるように設定
    return conn

def init_db():
    """ データベースのテーブルを初期化する """
    conn = get_db_connection()
    cursor = conn.cursor()

    
    # ユーザーテーブルの作成
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)    

    conn.commit()
    conn.close()
