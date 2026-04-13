import tkinter as tk
from gui.app import ProjectExtractorGUI

def main():
    root = tk.Tk()
    app = ProjectExtractorGUI(root)
    root.mainloop()
if __name__ == "__main__":
    main()
