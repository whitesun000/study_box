import os
import sys
from core.server_logic import ChatServer
from core.client_logic import ChatClient

# テスト用の共通鍵
SHARED_KEY = b'u76_Xo_21l8m8D9V1dO-0YmB7_yYI6T8_Zp2W3_v8lE='

def run_server():
    server = ChatServer(key=SHARED_KEY)
    server.start()
    # サーバーはスレッドで動くため、メインスレッドを維持
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\n[*] サーバーを停止します。")

def run_client():
    client = ChatClient(key=SHARED_KEY)
    name = input("あなたの名前を入力してください： ")
    
    if client.connect(name):
        print("[*] サーバーに接続しました。'exit'で終了します。")

        # メッセージ受信時の処理を登録
        client.on_message_received = lambda msg: print(f"\n{msg}\nメッセージ入力> ", end="")

        while True:
            msg = input("メッセージ入力> ")
            if msg.lower() == "exit":
                client.disconnect()
                break
            client.send_message(msg)

if __name__ == "__main__":
    print("=== Chat Tool ===")
    print("1: サーバー起動")
    print("2: クライアント起動")
    choice = input("選択してください (1 or 2): ")

    if choice == "1":
        run_server()
    elif choice == "2":
        run_client()
    else:
        print("無効な選択です。")