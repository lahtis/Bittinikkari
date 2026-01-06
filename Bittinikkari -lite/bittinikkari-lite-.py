# Bittinikkari lite - bittinikkari_lite.py
# Tekijä: Tuomas Lähteenmäki
# Version: 0.2
# Lisenssi: GNU GPLv3
import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import filedialog, messagebox, ttk
import os
import shutil

# --- LOGIIKKA (ENGINE) ---

def load_settings():
    return {
        "bg_color": "#2b2b2b",
        "fg_color": "#a9b7c6",
        "current_project": "Bittinikkari.cbp"
    }

def process_full_project(project_path):
    """Suorittaa yhden komennon taktiikan: varmuuskopiot ja siivous."""
    changes = 0
    if not os.path.exists(project_path):
        return 0
    try:
        tree = ET.parse(project_path)
        root = tree.getroot()
        proj_node = root.find("Project")
        if proj_node is not None:
            for unit in proj_node.findall("Unit"):
                f_path = unit.get("filename")
                if f_path and os.path.exists(f_path):
                    # Varmuuskopiointi (C-kieli muistinhallinta huomioiden)
                    shutil.copy2(f_path, f_path + ".bak")
                    with open(f_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                    with open(f_path, "w", encoding="utf-8") as f:
                        for line in lines:
                            f.write(line.rstrip() + "\n")
                    changes += 1
    except Exception as e:
        print(f"Virhe: {e}")
    return changes

# --- KÄYTTÖLIITTYMÄ (UI) ---

class BittinikkariEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Bittinikkari - GPL Editori")
        self.root.geometry("1000x700")
        self.settings = load_settings()
        
        # Työkalupalkki (Toolbar)
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Korjattu padx (ei px)
        tk.Button(toolbar, text="Avaa", command=self.open_file).pack(side=tk.LEFT, padx=5, pady=2)
        tk.Button(toolbar, text="Tallenna", command=self.save_file).pack(side=tk.LEFT, padx=5, pady=2)
        tk.Button(toolbar, text="⚡ Hienosäädä projekti", command=self.run_full_maintenance).pack(side=tk.LEFT, padx=5, pady=2)

        # Editorialue välilehdillä
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.new_file()

    def new_file(self, content="", title="Uusi", path=None):
        tab = tk.Frame(self.notebook)
        text_area = tk.Text(tab, bg=self.settings["bg_color"], fg=self.settings["fg_color"], 
                            insertbackground="white", font=("Consolas", 11), undo=True)
        text_area.pack(fill=tk.BOTH, expand=True)
        text_area.insert("1.0", content)
        
        tab.text_area = text_area
        tab.file_path = path
        
        self.notebook.add(tab, text=title)
        self.notebook.select(tab)

    def open_file(self):
        path = filedialog.askopenfilename()
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.new_file(content, os.path.basename(path), path)
            except Exception as e:
                messagebox.showerror("Virhe", f"Tiedostoa ei voitu avata: {e}")

    def save_file(self):
        tab_id = self.notebook.select()
        if not tab_id: return
        tab = self.notebook.nametowidget(tab_id)
        
        path = tab.file_path or filedialog.asksaveasfilename()
        if path:
            try:
                # Varmuuskopio ennen tallennusta
                if os.path.exists(path):
                    shutil.copy2(path, path + ".bak")
                
                content = tab.text_area.get("1.0", tk.END)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                
                tab.file_path = path
                self.notebook.tab(tab_id, text=os.path.basename(path))
                return True
            except Exception as e:
                messagebox.showerror("Virhe", f"Tallennus epäonnistui: {e}")
        return False

    def run_full_maintenance(self):
        """Kevyt muistinhallinta ja varmuuskopiot koko projektille."""
        path = self.settings["current_project"]
        if os.path.exists(path):
            count = process_full_project(path)
            messagebox.showinfo("Bittinikkari", f"Hienosäätö tehty {count} tiedostolle.\nVarmuuskopiot (.bak) luotu.")
        else:
            messagebox.showwarning("Projektia ei löydy", 
                                 f"Tiedostoa '{path}' ei löytynyt.\n\nVarmista että .cbp-tiedosto on samassa kansiossa.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BittinikkariEditor(root)

    root.mainloop()


