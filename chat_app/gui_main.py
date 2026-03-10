import tkinter as tk
from gui.layout import ChatLayout
from gui.controller import ChatController

# 共通鍵
SHARED_KEY = b'u76_Xo_21l8m8D9V1dO-0YmB7_yYI6T8_Zp2W3_v8lE='

def main():
    root = tk.Tk()

    # 司令塔を呼び出す
    app = ChatController(root, ChatLayout, SHARED_KEY)
    root.mainloop()

if __name__ == "__main__":
    main()