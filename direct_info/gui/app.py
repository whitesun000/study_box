import os
import tkinter as tk
from tkinter import filedialog, messagebox
from utils.file_processor import export_project_structure

class ProjectExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Content Extractor")
        self.root.geometry("500x350")

        # --- レイアウト ---
        # スキャン対象
        tk.Label(root, text="スキャン対象フォルダ:").pack(pady=(10, 0))
        self.target_entry = tk.Entry(root, width=50)
        self.target_entry.pack(pady=5)
        tk.Button(root, text="フォルダを選択", command=self.select_target).pack()

        # 保存先
        tk.Label(root, text="ログ保存先:").pack(pady=(10, 0))
        self.log_entry = tk.Entry(root, width=50)
        self.log_entry.insert(0, os.path.join(os.getcwd(), "logs", "project_content.log"))
        self.log_entry.pack(pady=5)
        tk.Button(root, text="保存先を選択", command=self.select_save_path).pack()

        # オプション：ファイルの中身を含めるか（チェックボックス）
        self.content_var = tk.BooleanVar(value=True)
        self.content_check = tk.Checkbutton(
            root,
            text = "ファイルの中身もログに書き込む",
            variable = self.content_var
        )
        self.content_check.pack(pady=10)

        # 実行ボタン
        tk.Button(root, text="スキャン開始", bg="skyblue", command=self.run_process).pack(pady=20)
    
    def select_target(self):
        path = filedialog.askdirectory()
        if path:
            self.target_entry.delete(0, tk.END)
            self.target_entry.insert(0, path)

    def select_save_path(self):
        default_name = "project_content.log"
        path = filedialog.asksaveasfilename(
            initialfile = default_name,
            defaultextension=".log",
            filetypes=[("Log files", "*.log"), ("Text files", "*.txt")]
        )
        if path:
            self.log_entry.delete(0, tk.END)
            self.log_entry.insert(0, path)

    def run_process(self):
        target = self.target_entry.get()
        log_path = self.log_entry.get()
        export_content = self.content_var.get()

        if not target or not os.path.exists(target):
            messagebox.showerror("エラー", "有効なスキャン対象フォルダを選択してください。")
            return
        
        try:
            export_project_structure(target, log_path, export_content=export_content)
            messagebox.showinfo("完了", f"ログを保存しました：\n{log_path}")
        except Exception as e:
            messagebox.showerror("エラー", f"実行中にエラーが発生しました:\n{e}")
