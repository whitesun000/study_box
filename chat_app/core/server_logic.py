import socket
import threading
from core.encryption import ChatCipher
from security.monitor import SecurityMonitor

class ChatServer:
    def __init__(self, host="0.0.0.0", port=9999, key=None):
        self.host = host
        self.port = port
        self.cipher = ChatCipher(key)
        self.monitor = SecurityMonitor()
        self.clients = {}
        self.running = False
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        try:
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            self.running = True
            print(f"[*] サーバー起動: {self.port}")

            # 接続待ちを別スレッドで実行 (GUIをフリーズさせないため)
            thread = threading.Thread(target=self._accept_connections, daemon=True)
            thread.start()
        except Exception as e:
            print(f"[!] サーバー起動に失敗しました: {e}")

    def _accept_connections(self):
        while self.running:
            try:
                client_socket, addr = self.server.accept()
                thread = threading.Thread(target=self._handle_client, args=(client_socket, addr), daemon=True)
                thread.start()
            except:
                break
    
    def _handle_client(self, client_socket, addr):
        ip = addr[0]
        try:
            # 最初のデータ（暗号化された名前）を受信
            encrypted_name = client_socket.recv(1024)
            if not encrypted_name:
                return
            
            user_name = self.cipher.decrypt_msg(encrypted_name)
            self.clients[client_socket] = user_name
            self.broadcast(f"--- {user_name} さんが参加しました ---", client_socket)

            while True:
                encrypted_data = client_socket.recv(1024)
                if not encrypted_data:
                    break
                    
                # セキュリティチェック（連打検知）
                if self.monitor.check_speed(ip):
                    if self.monitor.add_score(ip, 20, "高速連打"):
                        break
                
                # 復号と内容チェック
                message = self.cipher.decrypt_msg(encrypted_data)
                if "'" in message or "--" in message:
                    self.monitor.add_score(ip, 50, "不審な記号")

                self.broadcast(f"{user_name}: {message}", client_socket)
        
        except Exception as e:
            print(f"[!] エラー: {e}")
        finally:
            if client_socket in self.clients:
                del self.clients[client_socket]
            client_socket.close()
    
    def broadcast(self, message, sender_socket):
        print(f"[Broadcast] {message}")
        encrypted_msg = self.cipher.encrypt_msg(message)
        for c in self.clients:
            if c != sender_socket:
                try:
                    c.send(encrypted_msg)
                except:
                    pass
