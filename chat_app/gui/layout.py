import tkinter as tk
from tkinter import scrolledtext

class ChatLayout:
    def __init__(self, root, send_callback, server_start_callback, client_start_callback):
        self.root = root
        self.root.title("Python 暗号化チャット - 統合コンソール")

        # --- モード選択エリア ---
        self.mode_frame = tk.Frame(root)
        self.mode_frame.pack(padx=10, pady=10, fill=tk.X)

        self.btn_server = tk.Button(self.mode_frame, text="サーバー起動", command=server_start_callback, bg="lightgrey")
        self.btn_server.pack(side=tk.LEFT, padx=5)

        self.btn_client = tk.Button(self.mode_frame, text="クライアントとして参加", command=client_start_callback, bg="lightblue")
        self.btn_client.pack(side=tk.LEFT, padx=5)

        # --- チャット表示エリア ---
        self.chat_area = scrolledtext.ScrolledText(root, state='disabled', height=15)
        self.chat_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # --- メッセージ入力エリア ---
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(padx=10, pady=5, fill=tk.X)

        self.entry_msg = tk.Entry(self.input_frame)
        self.entry_msg.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.btn_send = tk.Button(root, text="送信", command=send_callback)
        self.btn_send.pack(side=tk.RIGHT, pady=5)
    
    def update_chat(self, message):
        """ チャット画面に文字を追加する """
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)

    def enable_send(self):
        self.btn_send.config(state=tk.NORMAL)
        