import os
import sqlite3
from app.core.config import settings

def get_db_connection():
    # フォルダが存在するかチェックし、なければ作成する
    db_dir = "data"
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        print(f"Directory '{db_dir}' created.")

    # .env や config で設定したパスを使ってDBに接続
    conn = sqlite3.connect("data/chat_app.sqlite3")
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

    # テストユーザーがいなければ作成
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "password123"))
    

    conn.commit()
    conn.close()
