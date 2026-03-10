import tkinter as tk
from core.server_logic import ChatServer
from core.client_logic import ChatClient
from tkinter import messagebox, simpledialog

class ChatController:
    def __init__(self, root, layout_class, key):
        self.root = root
        self.key = key
        self.server = None
        self.client = None

        self.view = layout_class(root, self.handle_send, self.launch_server, self.launch_client)

    def launch_server(self):
        """ サーバーをバックグランドで起動 """
        try:
            self.server = ChatServer(key=self.key)
            self.server.start()
            self.view.update_chat("[システム] サーバーを起動しました(ポート:9999)")
        except Exception as e:
            messagebox.showerror("エラー", f"サーバー起動失敗: {e}")
    
    def launch_client(self):
        """ クライアントとして接続 """
        user_name = simpledialog.askstring("名前入力", "チャットでの名前を入力してください:")
        if not user_name: return

        self.client = ChatClient(key=self.key)
        self.client.on_message_received = self.view.update_chat

        if self.client.connect(user_name):
            self.view.update_chat(f"[システム] {user_name} として接続しました。")
            self.view.enable_send()
        else:
            messagebox.showerror("エラー", "接続に失敗しました。サーバーが起動しているか確認してください。")

    def handle_send(self):
        msg = self.view.entry_msg.get()
        if msg and self.client:
            self.client.send_message(msg)
            self.view.update_chat(f"自分: {msg}")
            self.view.entry_msg.delete(0, tk.END)

