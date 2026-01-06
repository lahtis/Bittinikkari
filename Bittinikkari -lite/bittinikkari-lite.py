# -*- coding: utf-8 -*-
"""
Bittinikkari Lite - bittinikkari-lite.py
Author: Tuomas Lähteenmäki
Version: 0.2
License: GNU GPLv3

Description:
A minimalist, standalone code editor designed for quick edits.
Features: Zero-dependencies, automatic backups, and whitespace optimization.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil

# --- LOGIC (ENGINE) ---

def load_settings():
    """Returns default editor styling settings."""
    return {
        "bg_color": "#2b2b2b",
        "fg_color": "#a9b7c6"
    }

# --- USER INTERFACE (UI) ---

class BittinikkariLite:
    def __init__(self, root):
        self.root = root
        self.root.title("Bittinikkari Lite")
        self.root.geometry("800x600")
        self.settings = load_settings()
        
        # --- ICON SUPPORT ---
        # Try to load 'icon.ico' from the same directory as this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "icon.ico")
        
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception as e:
                print(f"Icon load error: {e}")

        # Toolbar
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Action Buttons
        tk.Button(toolbar, text="Open", command=self.open_file).pack(side=tk.LEFT, padx=5, pady=2)
        tk.Button(toolbar, text="Save", command=self.save_file).pack(side=tk.LEFT, padx=5, pady=2)
        tk.Button(toolbar, text="⚡ Optimize", command=self.optimize_current_file).pack(side=tk.LEFT, padx=5, pady=2)

        # Editor Area
        self.text_area = tk.Text(self.root, bg=self.settings["bg_color"], 
                                 fg=self.settings["fg_color"], 
                                 insertbackground="white", 
                                 font=("Consolas", 11), undo=True)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        self.current_file_path = None

    def open_file(self):
        """Opens a file and displays its content."""
        path = filedialog.askopenfilename()
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", content)
                self.current_file_path = path
                self.root.title(f"Bittinikkari Lite - {os.path.basename(path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")

    def save_file(self):
        """Saves the current content and creates a backup file."""
        path = self.current_file_path or filedialog.asksaveasfilename()
        if path:
            try:
                # Backup existing file before overwrite
                if os.path.exists(path):
                    shutil.copy2(path, path + ".bak")
                
                content = self.text_area.get("1.0", tk.END)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                
                self.current_file_path = path
                self.root.title(f"Bittinikkari Lite - {os.path.basename(path)}")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Save failed: {e}")
        return False

    def optimize_current_file(self):
        """Removes trailing whitespaces from the current editor text."""
        content = self.text_area.get("1.0", tk.END).splitlines()
        optimized_content = "\n".join([line.rstrip() for line in content])
        
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", optimized_content)
        messagebox.showinfo("Lite Optimizer", "Trailing whitespaces removed!")

if __name__ == "__main__":
    root = tk.Tk()
    app = BittinikkariLite(root)
    root.mainloop()