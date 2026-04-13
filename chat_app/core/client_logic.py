import socket
import threading 
from core.encryption import ChatCipher

class ChatClient:
    def __init__(self, ip="127.0.0.1", port=9999, key=None):
        self.ip = ip
        self.port = port
        self.cipher = ChatCipher(key)
        self.client_socket = None
        self.is_connected = False
        # GUIにメッセージを渡すための「コールバック関数」を保持する
        self.on_message_received = None
    
    def connect(self, user_name):
        """ サーバーに接続し、名前を送信する """
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.ip, self.port))
            self.is_connected = True

            # 最初の名前を暗号化して送信
            self.client_socket.send(self.cipher.encrypt_msg(user_name))

            # 受信専用のスレッドを開始
            thread = threading.Thread(target=self._receive_loop, daemon=True)
            thread.start()
            return True
        except Exception as e:
            print(f"接続エラー: {e}")
            return False
        
    def send_message(self, message):
        """ メッセージを暗号化して送信する """
        if self.is_connected:
            try:
                encrypted_msg = self.cipher.encrypt_msg(message)
                self.client_socket.send(encrypted_msg)
            except Exception as e:
                print(f"送信エラー: {e}")
                self.is_connected = False
        
    def _receive_loop(self):
        """ サーバーからのメッセージを受け取り続ける """
        while self.is_connected:
            try:
                encrypted_data = self.client_socket.recv(1024)
                if not encrypted_data:
                    break

                # 復号
                message = self.cipher.decrypt_msg(encrypted_data)

                # もしメッセージを受け取ったときの処理（コールバック）が登録されていれば実行
                if self.on_message_received:
                    self.on_message_received(message)
                else:
                    # 登録がなければとりあえずターミナルに出す
                    print(f"\n{message}")
            except Exception as e:
                print(f"受信エラー: {e}")
                break
    
    def disconnect(self):
        """ 安全に切断する """
        self.is_connected = False
        if self.client_socket:
            self.client_socket.close()
