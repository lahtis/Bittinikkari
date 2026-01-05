# Bittinikkari - editor_ui.py
# Tekijä: Tuomas Lähteenmäki
# Lisenssi: GNU GPLv3

import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import filedialog, messagebox, ttk
import os
import re
from engine import run_fixing_logic, load_settings



def process_full_project(project_path, settings):
    """Suorittaa yhden komennon taktiikan mukaisen hienosäädön [cite: 2026-01-05]."""
    changes = 0
    reports = ["--- Bittinikkari Raportti 2026 ---"]
    
    # Esimerkki: Varmuuskopiointi ja kevyt C-tarkistus
    reports.append(f"Analysoidaan projekti: {project_path}")
    # Logiikka sisennyksille, lisensseille ja muistinhallinnalle...
    
    return changes, reports
    
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text: return
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tk.Label(tw, text=self.text, background="#ffffe0", relief=tk.SOLID, borderwidth=1).pack()

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

class BittinikkariEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Bittinikkari - Tekstieditori (GPL)")
        self.root.geometry("1200x800")
        self.settings = load_settings()
        
        # Pääkontti
        self.main_container = tk.Frame(self.root, bg=self.settings.get("bg_color", "#f0f0f0"))
        self.main_container.pack(fill=tk.BOTH, expand=True)

        self.create_toolbar()

        # PanedWindow: Sivupalkki | Editori
        self.paned_window = tk.PanedWindow(self.main_container, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Sivupalkki
        self.sidebar = ttk.Notebook(self.paned_window)
        self.create_sidebar_content()
        self.paned_window.add(self.sidebar, width=250)

        # Editori-alue
        editor_container = tk.Frame(self.paned_window)
        tab_control = tk.Frame(editor_container, bg="#313335")
        tab_control.pack(side=tk.TOP, fill=tk.X)
        
        self.close_btn = tk.Button(tab_control, text=" ✕ Sulje välilehti ", 
                                   command=self.close_current_tab, 
                                   bg="#c42b1c", fg="white", relief=tk.FLAT, padx=10)
        self.close_btn.pack(side=tk.RIGHT, padx=5, pady=2)

        self.nikkari_btn = tk.Button(tab_control, text=" 🛠 NIKKAROI ", 
                                     command=self.nikkaroi_action, 
                                     bg="#0078d4", fg="white", relief=tk.FLAT, font=("Arial", 9, "bold"), padx=10)
        self.nikkari_btn.pack(side=tk.RIGHT, padx=5, pady=2)

        self.notebook = ttk.Notebook(editor_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.paned_window.add(editor_container)
        
        self.create_menu()
        self.status_bar = tk.Label(self.root, text="Valmis", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Pikanäppäimet
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-f>", lambda e: self.find_text())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Alt-n>", lambda e: self.nikkaroi_action())
        self.root.bind("<F5>", lambda e: self.nikkaroi_action())
        
        self.new_file()

    def create_toolbar(self):
        toolbar = tk.Frame(self.main_container, bd=1, relief=tk.RAISED)
        buttons = [
            ("U", "Uusi (Ctrl+N)", self.new_file),
            ("A", "Avaa", self.open_file),
            ("T", "Tallenna (Ctrl+S)", self.save_file),
            ("N", "Nikkaroi (Fiksi)", self.nikkaroi_action)
        ]
        for txt, hint, cmd in buttons:
            btn = tk.Button(toolbar, text=txt, command=cmd, width=3, relief=tk.FLAT)
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            ToolTip(btn, hint)
        toolbar.pack(side=tk.TOP, fill=tk.X)

    def add_quick_fix_button(self):
        # Työkalupalkin nappi (jos sinulla on Toolbar-frame)
        fix_btn = tk.Button(self.toolbar, text="⚡ Hienosäädä projekti", 
                            command=self.run_full_maintenance,
                            bg="#e1f5fe", relief=tk.FLAT)
        fix_btn.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Pikanäppäin
        self.root.bind("<Control-Shift-B>", lambda e: self.run_full_maintenance())

    def run_full_maintenance(self):
        """Suorittaa varmuuskopiot, sisennykset, lisenssit ja C-tarkistukset."""
        project_path = self.settings.get("current_project", "Bittinikkari.cbp")
        
        if not os.path.exists(project_path):
            messagebox.showwarning("Bittinikkari", "Projektitiedostoa ei löydy.")
            return

        confirm = messagebox.askyesno("Vahvistus", "Suoritetaanko koko projektin hienosäätö?\n\n"
                                     "- Varmuuskopiot luodaan\n"
                                     "- Sisennykset korjataan\n"
                                     "- Lisenssit tarkistetaan\n"
                                     "- C-muistinhallinta analysoidaan")
        if confirm:
            from modules.engine import process_full_project
            changes, reports = process_full_project(project_path, self.settings)
            
            # Näytetään tulokset
            report_text = "\n".join(reports[:15])
            messagebox.showinfo("Valmis", f"Muutoksia tehty: {changes}\n\nRaportti:\n{report_text}")

    def create_sidebar_content(self):
        self.projects_tab = ttk.Frame(self.sidebar)
        self.files_tab = ttk.Frame(self.sidebar)
        self.sidebar.add(self.projects_tab, text="Projects")
        self.sidebar.add(self.files_tab, text="Files")
        self.file_tree = ttk.Treeview(self.files_tab)
        self.file_tree.pack(fill=tk.BOTH, expand=True)
        self.file_tree.heading("#0", text="Projektin tiedostot", anchor='w')
        self.file_tree.bind("<Double-1>", self.on_tree_double_click)
        self.refresh_file_tree()

    def refresh_file_tree(self):
        self.file_tree.delete(*self.file_tree.get_children())
        folder_path = os.getcwd()
        root_node = self.file_tree.insert("", "end", text=os.path.basename(folder_path), open=True)
        for item in os.listdir(folder_path):
            if not item.startswith("."):
                abs_path = os.path.join(folder_path, item)
                self.file_tree.insert(root_node, "end", text=item, values=(abs_path,))

    def on_tree_double_click(self, event):
        item_id = self.file_tree.focus()
        item_data = self.file_tree.item(item_id)
        if item_data["values"]:
            file_path = item_data["values"][0]
            if os.path.isfile(file_path):
                self.open_specific_file(file_path)

    def new_file(self, content=None, title="Uusi tiedosto", path=None):
        tab = tk.Frame(self.notebook, bg=self.settings.get("bg_color", "#2b2b2b"))
        y_scroll = tk.Scrollbar(tab)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        x_scroll = tk.Scrollbar(tab, orient=tk.HORIZONTAL)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        folding_bar = tk.Canvas(tab, width=20, bg="#313335", highlightthickness=0)
        folding_bar.pack(side=tk.LEFT, fill=tk.Y)
        line_nums = tk.Canvas(tab, width=40, bg="#313335", highlightthickness=0)
        line_nums.pack(side=tk.LEFT, fill=tk.Y)
        change_bar = tk.Canvas(tab, width=5, bg="#313335", highlightthickness=0)
        change_bar.pack(side=tk.LEFT, fill=tk.Y)

        text_area = tk.Text(tab, undo=True, wrap=tk.NONE, font=("Courier New", 12),
                            yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set,
                            bg=self.settings.get("bg_color", "#2b2b2b"),
                            fg=self.settings.get("fg_color", "#a9b7c6"),
                            insertbackground="white", padx=5)
        
        y_scroll.config(command=text_area.yview)
        x_scroll.config(command=text_area.xview)
        text_area.pack(fill=tk.BOTH, expand=True)

        def trigger_update(*args):
            self.update_lines(text_area, line_nums, change_bar, folding_bar)

        def mark_line_modified(event):
            if event.char and event.keysym not in ("Control_L", "Control_R", "Shift_L", "Shift_R"):
                text_area.tag_add("modified_line", "insert linestart", "insert lineend")
                self.root.after(10, trigger_update)

        def on_modified(event):
            if text_area.edit_modified():
                text_area.tag_remove('match', '1.0', tk.END)
                self.root.after(1, trigger_update)

        text_area.bind("<Key>", mark_line_modified)
        text_area.bind("<KeyRelease>", trigger_update)
        text_area.bind("<MouseWheel>", trigger_update)
        text_area.bind("<<Modified>>", on_modified)
        
        self.create_context_menu(text_area)

        tab.text_area = text_area
        tab.line_nums = line_nums
        tab.change_bar = change_bar
        tab.folding_bar = folding_bar
        tab.file_path = path

        if content: 
            text_area.insert(1.0, content)
            text_area.edit_modified(False) 
        
        self.apply_syntax_highlighting(text_area)
        self.notebook.add(tab, text=title)
        self.notebook.select(tab)
        self.root.after(100, trigger_update)

    def update_lines(self, text_area, line_nums, change_bar, folding_bar):
        line_nums.delete("all")
        change_bar.delete("all")
        folding_bar.delete("all")
        
        is_modified_globally = text_area.edit_modified()
        i = text_area.index("@0,0")
        while True:
            dline = text_area.dlineinfo(i)
            if dline is None: break
            y1, y2 = dline[1], dline[1] + dline[3]
            line_num = str(i).split(".")[0]
            line_nums.create_text(35, y1, anchor="ne", text=line_num, fill="gray")
            
            has_tag = "modified_line" in text_area.tag_names(f"{line_num}.0")
            if not is_modified_globally:
                color = "green"
                text_area.tag_remove("modified_line", f"{line_num}.0", f"{line_num}.end")
            else:
                color = "red" if has_tag else "#313335"
            change_bar.create_rectangle(0, y1, 5, y2, fill=color, outline="")
            i = text_area.index("%s+1line" % i)

    def open_settings(self):
        messagebox.showinfo("Asetukset", "Asetuspaneeli tulossa päivityksessä (2026).")

    def check_updates(self):
        messagebox.showinfo("Päivitys", "Bittinikkari on ajan tasalla (v1.1.0)")

    def open_file(self):
        """Avaa tiedostonvalintaikkunan ja lataa valitun tiedoston."""
        path = filedialog.askopenfilename(
            filetypes=[
                ("Kaikki tiedostot", "*.*"),
                ("Python tiedostot", "*.py"),
                ("C tiedostot", "*.c"),
                ("JSON tiedostot", "*.json")
            ]
        )
        if path:
            self.open_specific_file(path)

    def open_specific_file(self, path):
        """Lukee tiedoston sisällön ja avaa uuden välilehden."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.new_file(content=content, title=os.path.basename(path), path=path)
            self.update_status(f"Avattu: {path}")
        except Exception as e:
            messagebox.showerror("Virhe", f"Tiedostoa ei voitu avata: {e}")

    def save_file(self, save_as=False):
        """Tallentaa nykyisen tiedoston. Luo automaattisesti .bak-varmuuskopion."""
        import shutil
        try:
            text_widget = self.get_current_text_widget()
            path = self.get_current_file_path()
            
            if not path or save_as:
                path = filedialog.asksaveasfilename(
                    defaultextension=".py",
                    filetypes=[("Python", "*.py"), ("C", "*.c"), ("Kaikki", "*.*")]
                )
                
            if path:
                # Varmuuskopiointi ennen tallennusta
                if os.path.exists(path):
                    try:
                        shutil.copy2(path, path + ".bak")
                    except:
                        pass # Varmuuskopiointi epäonnistui, jatketaan silti

                content = text_widget.get(1.0, tk.END)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)
                
                self.set_current_file_path(path)
                text_widget.edit_modified(False)
                self.update_status(f"Tallennettu: {os.path.basename(path)}")
                return True
        except Exception as e:
            messagebox.showerror("Tallennusvirhe", str(e))
        return False

    def create_context_menu(self, text_widget):
        context_menu = tk.Menu(text_widget, tearoff=0)
        context_menu.add_command(label="Leikkaa", command=lambda: text_widget.event_generate("<<Cut>>"))
        context_menu.add_command(label="Kopioi", command=lambda: text_widget.event_generate("<<Copy>>"))
        context_menu.add_command(label="Liitä", command=lambda: text_widget.event_generate("<<Paste>>"))
        context_menu.add_separator()
        context_menu.add_command(label="Etsi...", command=self.find_text)
        context_menu.add_command(label="Valitse kaikki", command=lambda: text_widget.tag_add("sel", "1.0", tk.END))
        def show_popup(event):
            text_widget.focus_set()
            context_menu.tk_popup(event.x_root, event.y_root)
            return "break"
        text_widget.bind("<Button-3>", show_popup)

    def find_text(self):
        text_widget = self.get_current_text_widget()
        selected_text = ""
        try:
            if text_widget.tag_ranges("sel"):
                selected_text = text_widget.get("sel.first", "sel.last")
        except: pass

        find_win = tk.Toplevel(self.root)
        find_win.title("Etsi ja Korvaa")
        find_win.geometry("450x230")
        find_win.attributes('-topmost', True)
        main_frame = tk.Frame(find_win, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="Etsi:").grid(row=0, column=0, sticky="w", pady=5)
        find_entry = tk.Entry(main_frame, width=30)
        find_entry.grid(row=0, column=1, padx=5, pady=5)
        if selected_text:
            find_entry.insert(0, selected_text)
            find_entry.selection_range(0, tk.END)

        tk.Label(main_frame, text="Korvaa:").grid(row=1, column=0, sticky="w", pady=5)
        replace_entry = tk.Entry(main_frame, width=30)
        replace_entry.grid(row=1, column=1, padx=5, pady=5)

        regex_var = tk.BooleanVar(value=False)
        tk.Checkbutton(main_frame, text="Regex haku", variable=regex_var).grid(row=2, column=1, sticky="w")

        def do_find(event=None):
            text_widget.tag_remove('match', '1.0', tk.END)
            s = find_entry.get()
            if not s: return
            idx = '1.0'
            use_regex = regex_var.get()
            while True:
                idx = text_widget.search(s, idx, stopindex=tk.END, nocase=True, regexp=use_regex)
                if not idx: break
                if use_regex:
                    content_after = text_widget.get(idx, f"{idx} lineend")
                    match_obj = re.search(s, content_after, re.IGNORECASE)
                    match_len = len(match_obj.group(0)) if match_obj else 1
                else: match_len = len(s)
                lastidx = f"{idx}+{match_len}c"
                text_widget.tag_add('match', idx, lastidx)
                idx = lastidx
            text_widget.tag_config('match', background='yellow', foreground='black')

        def do_replace_all():
            search_str = find_entry.get()
            replace_str = replace_entry.get()
            if not search_str: return
            content = text_widget.get("1.0", tk.END)
            new_content = content.replace(search_str, replace_str)
            text_widget.delete("1.0", tk.END)
            text_widget.insert("1.0", new_content)
            text_widget.tag_remove('match', '1.0', tk.END)
            text_widget.edit_modified(True)

        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(btn_frame, text="Etsi", command=do_find, width=10).pack(side=tk.LEFT, padx=2)
        tk.Button(btn_frame, text="Korvaa kaikki", command=do_replace_all, width=12).pack(side=tk.LEFT, padx=2)
        find_entry.bind("<Return>", do_find)
        find_entry.focus_set()

    def nikkaroi_action(self):
        text_widget = self.get_current_text_widget()
        content = text_widget.get("1.0", tk.END)
        if self.save_file():
            if "malloc" in content and "free" not in content:
                messagebox.showwarning("Bittinikkari: Muistinhallinta", "Koodissa on 'malloc', mutta 'free' puuttuu!")
            lines = content.split('\n')
            new_content = '\n'.join([line.rstrip() for line in lines])
            text_widget.delete("1.0", tk.END)
            text_widget.insert("1.0", new_content)
            self.update_status("Nikkarointi valmis.")

    def apply_syntax_highlighting(self, text_area):
        syntax_colors = self.settings.get("syntax", {})
        for tag, color in syntax_colors.items():
            text_area.tag_configure(tag, foreground=color)
        rules = [(r'\b(def|class|if|else|elif|while|for|return|int|char|void)\b', 'keyword'),
                 (r'\b(malloc|free)\b', 'memory'), (r'\".*?\"', 'string'), (r'#.*|//.*', 'comment')]
        def highlight():
            content = text_area.get("1.0", tk.END)
            for pattern, tag in rules:
                for m in re.finditer(pattern, content):
                    text_area.tag_add(tag, f"1.0+{m.start()}c", f"1.0+{m.end()}c")
        text_area.bind("<KeyRelease>", lambda e: highlight(), add="+")
        self.root.after(200, highlight)

    def show_project_context_menu(self, event):
        item = self.project_tree.identify_row(event.y)
        if item:
            self.project_tree.selection_set(item)
            self.project_menu.post(event.x_root, event.y_root)

    def remove_from_project(self):
        """Poistaa valitun tiedoston .cbp-tiedostosta."""
        item_id = self.project_tree.focus()
        item_data = self.project_tree.item(item_id)
        file_to_remove = item_data["values"][0] if item_data["values"] else None
        
        if not file_to_remove:
            return

        if messagebox.askyesno("Vahvista", f"Poistetaanko '{file_to_remove}' projektista?\n(Tiedosto jää levylle.)"):
            project_path = self.settings.get("current_project")
            try:
                tree = ET.parse(project_path)
                root = tree.getroot()
                proj_node = root.find("Project")
                
                # Etsitään ja poistetaan oikea Unit-tagi
                for unit in proj_node.findall("Unit"):
                    if unit.get("filename") == file_to_remove:
                        proj_node.remove(unit)
                        break
                
                # Tallennetaan muutokset
                tree.write(project_path, encoding="UTF-8", xml_declaration=True)
                self.load_cbp_project(project_path) # Päivitetään näkymä
                self.update_status(f"Poistettu projektista: {file_to_remove}")
            except Exception as e:
                messagebox.showerror("Virhe", f"Poisto epäonnistui: {e}")

    def populate_files_tab(self, path):
        """Täyttää Files-välilehden kansion sisällöllä."""
        for i in self.files_tree.get_children():
            self.files_tree.delete(i)
            
        root_node = self.files_tree.insert("", "end", text=path, open=True)
        try:
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                is_dir = os.path.isdir(full_path)
                self.files_tree.insert(root_node, "end", text=item, values=(full_path,))
        except Exception as e:
            self.files_tree.insert(root_node, "end", text=f"Virhe: {e}")

    def create_sidebar_content(self):
        self.projects_tab = ttk.Frame(self.sidebar)
        self.files_tab = ttk.Frame(self.sidebar)
        self.sidebar.add(self.projects_tab, text="Project")
        self.sidebar.add(self.files_tab, text="Files")

        # --- PROJECT-VÄLILEHTI ---
        self.project_tree = ttk.Treeview(self.projects_tab)
        self.project_tree.pack(fill=tk.BOTH, expand=True)
        self.project_tree.heading("#0", text="Bittinikkari - tiedostot", anchor='w')
        
        # Project-valikko (Oikea nappi)
        self.project_menu = tk.Menu(self.project_tree, tearoff=0)
        self.project_menu.add_command(label="Avaa editoriin", command=lambda: self.on_project_tree_double_click(None))
        self.project_menu.add_command(label="Poista projektista", command=self.remove_from_project)
        
        self.project_tree.bind("<Button-3>", self.show_project_context_menu)
        self.project_tree.bind("<Double-1>", self.on_project_tree_double_click)

        # --- FILES-VÄLILEHTI ---
        self.files_tree = ttk.Treeview(self.files_tab)
        self.files_tree.pack(fill=tk.BOTH, expand=True)
        self.files_tree.heading("#0", text="Tiedostojärjestelmä", anchor='w')
        
        # Files-valikko (Oikea nappi)
        self.files_context_menu = tk.Menu(self.files_tree, tearoff=0)
        self.files_context_menu.add_command(label="Avaa hätätilassa", command=self.open_from_files_tab)
        self.files_context_menu.add_command(label="Lisää projektiin", command=self.add_selected_to_project)
        
        self.files_tree.bind("<Button-3>", self.show_files_context_menu)
        self.files_tree.bind("<Double-1>", lambda e: self.open_from_files_tab())

        # Alkutilan lataus
        # Muuta create_sidebar_content -metodissa:
        last_project = self.settings.get("current_project", "Bittinikkari.cbp")
        if os.path.exists(last_project):
            self.load_cbp_project(last_project)
            
        self.populate_files_tab(os.getcwd())

    # --- UUDET TOIMINNOT ---

    def show_files_context_menu(self, event):
        item = self.files_tree.identify_row(event.y)
        if item:
            self.files_tree.selection_set(item)
            self.files_context_menu.post(event.x_root, event.y_root)

    def open_from_files_tab(self):
        """Avaa tiedoston Files-välilehdeltä projektiin kajoamatta."""
        item_id = self.files_tree.focus()
        item_data = self.files_tree.item(item_id)
        if item_data["values"]:
            file_path = item_data["values"][0]
            if os.path.isfile(file_path):
                self.open_specific_file(file_path)

    def add_selected_to_project(self):
        """Lisää Files-välilehdellä valitun tiedoston .cbp-projektiin."""
        item_id = self.files_tree.focus()
        item_data = self.files_tree.item(item_id)
        if item_data["values"]:
            file_path = item_data["values"][0]
            # Hyödynnetään aiempaa add_file_to_project -logiikkaa mutta suoralla polulla
            self.do_add_file_to_cbp(file_path)

    def show_project_context_menu(self, event):
        item = self.project_tree.identify_row(event.y)
        if item:
            self.project_tree.selection_set(item)
            self.project_menu.post(event.x_root, event.y_root)

    def load_cbp_project(self, filename):
        if not os.path.exists(filename):
            self.project_tree.insert("", "end", text="Projektitiedosto puuttuu")
            return

        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            
            # Haetaan projektin nimi (tiedostossa "Bittinikkatri" )
            proj_node = root.find("Project")
            title = proj_node.find("Option").get("title", "Bittinikkari")
            
            main_node = self.project_tree.insert("", "end", text=title, open=True)

            # Ryhmitellään tiedostot kansioiden mukaan visuaalisesti
            folders = {}
            
            for unit in proj_node.findall("Unit"):
                filepath = unit.get("filename")
                parts = filepath.split('/')
                
                if len(parts) > 1:
                    # On kansion sisällä (esim. src/ai/factory.py)
                    parent_path = "/".join(parts[:-1])
                    if parent_path not in folders:
                        folders[parent_path] = self.project_tree.insert(main_node, "end", text=parent_path, open=False)
                    self.project_tree.insert(folders[parent_path], "end", text=parts[-1], values=(filepath,))
                else:
                    # Juuritasolla (esim. main.py)
                    self.project_tree.insert(main_node, "end", text=filepath, values=(filepath,))
                    
        except Exception as e:
            print(f"Virhe CBP-tiedoston luvussa: {e}")

    def on_project_tree_double_click(self, event):
        item_id = self.project_tree.focus()
        item_data = self.project_tree.item(item_id)
        if item_data["values"]:
            file_path = item_data["values"][0]
            if os.path.exists(file_path):
                self.open_specific_file(file_path)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Uusi", command=self.new_file)
        file_menu.add_command(label="Avaa", command=self.open_file)
        file_menu.add_command(label="Tallenna", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Lopeta", command=self.root.quit)
        menubar.add_cascade(label="Tiedosto", menu=file_menu)
        
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Etsi ja Korvaa...", command=self.find_text, accelerator="Ctrl+F")
        menubar.add_cascade(label="Muokkaa", menu=edit_menu)

        project_menu = tk.Menu(menubar, tearoff=0)
        project_menu.add_command(label="Luo uusi projekti...", command=self.create_new_project)
        project_menu.add_command(label="Avaa projekti (.cbp)...", command=lambda: self.load_cbp_project(filedialog.askopenfilename()))
        project_menu.add_separator()
        project_menu.add_command(label="Lisää tiedosto projektiin...", command=self.add_file_to_project)
        menubar.add_cascade(label="Projekti", menu=project_menu)

        menubar.add_command(label="Asetukset", command=self.open_settings)
        
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="Tietoa", command=self.show_about)
        about_menu.add_command(label="Päivitys", command=self.check_updates)
        menubar.add_cascade(label="About", menu=about_menu)
        self.root.config(menu=menubar)

    def get_current_text_widget(self):
        return self.notebook.nametowidget(self.notebook.select()).text_area

    def get_current_file_path(self):
        return self.notebook.nametowidget(self.notebook.select()).file_path

    def set_current_file_path(self, path):
        tab = self.notebook.nametowidget(self.notebook.select())
        tab.file_path = path
        self.notebook.tab(tab, text=os.path.basename(path))

    def update_status(self, msg):
        path = self.get_current_file_path()
        backup_str = " | [Backup OK]" if path and os.path.exists(path + ".bak") else ""
        self.status_bar.config(text=f"{msg}{backup_str}")

    def close_current_tab(self):
        current_index = self.notebook.index(self.notebook.select())
        tab_id = self.notebook.tabs()[current_index]
        tab = self.notebook.nametowidget(tab_id)
        if tab.text_area.edit_modified():
            if messagebox.askyesno("Tallennus", "Tallennetaanko muutokset?"):
                self.save_file()
        self.notebook.forget(current_index)

    def show_about(self):
        about_win = tk.Toplevel(self.root)
        about_win.title("Tietoa ohjelmasta")
        about_win.geometry("550x500")
        about_win.attributes('-topmost', True)
        
        # Yläosan tiedot
        info_text = "Bittinikkari v1.1\n© 2026 Tuomas Lähteenmäki\n"
        tk.Label(about_win, text=info_text, font=("Arial", 10, "bold"), pady=10).pack()

        # Lisenssialue
        tk.Label(about_win, text="Ohjelmistolisenssi:").pack(anchor="w", padx=15)
        
        license_frame = tk.Frame(about_win)
        license_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        scrollbar = tk.Scrollbar(license_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        license_area = tk.Text(license_frame, height=15, font=("Courier", 9), 
                               yscrollcommand=scrollbar.set, wrap=tk.WORD,
                               bg="#f9f9f9", padx=5, pady=5)
        license_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=license_area.yview)

        # LADATAAN LISENSSI TIEDOSTOSTA
        license_filename = "LICENSE.txt" # Voit käyttää myös "LICENSE" ilman päätettä
        if os.path.exists(license_filename):
            try:
                with open(license_filename, "r", encoding="utf-8") as f:
                    gpl_text = f.read()
            except Exception as e:
                gpl_text = f"Virhe lisenssitiedoston lukemisessa: {e}"
        else:
            gpl_text = f"HUOMIO: Lisenssitiedostoa ({license_filename}) ei löytynyt projektin juuresta."

        license_area.insert(tk.END, gpl_text)
        license_area.config(state=tk.DISABLED) # Vain luku -tila

        # Sulje-painike
        tk.Button(about_win, text="Sulje", command=about_win.destroy, width=12).pack(pady=10)

    def create_new_project(self):
        """Luo uuden bittinikkari-projektitiedoston (.cbp)."""
        path = filedialog.asksaveasfilename(
            defaultextension=".cbp",
            filetypes=[("CodeBlocks Project", "*.cbp")],
            title="Luo uusi projekti"
        )
        if path:
            root = ET.Element("CodeBlocks_project_file")
            proj = ET.SubElement(root, "Project")
            opt = ET.SubElement(proj, "Option")
            opt.set("title", os.path.basename(path).replace(".cbp", ""))
            
            # Luodaan perusrakenne
            tree = ET.ElementTree(root)
            tree.write(path, encoding="UTF-8", xml_declaration=True)
            
            self.settings["current_project"] = path
            self.load_cbp_project(path)
            self.update_status(f"Projekti luotu: {path}")

    def fix_entire_project_action(self):
        """Käyttöliittymän komento massakorjauksen käynnistämiseen."""
        path = self.settings.get("current_project")
        if not path:
            messagebox.showwarning("Bittinikkari", "Avaa projekti ensin.")
            return

        if messagebox.askyesno("Vahvistus", "Hienosäädetäänkö koko bittinikkari-projekti?"):
            # Kutsutaan engineä
            changes, reports = process_full_project(path, self.settings)
            
            # Näytetään lopputulos
            report_msg = "\n".join(reports[:20]) # Näytetään vain 20 ensimmäistä riviä
            if len(reports) > 20: report_msg += "\n... (lista jatkuu)"
            
            messagebox.showinfo("Valmis", f"Muutoksia tehty: {total_changes}\n\nRaportti:\n{report_msg}")
            self.update_status(f"Massakorjaus valmis: {changes} muutosta.")

    def add_file_to_project(self):
        """Lisää valitun tiedoston nykyiseen .cbp-projektiin."""
        project_path = self.settings.get("current_project", "Bittinikkari.cbp")
        
        if not os.path.exists(project_path):
            messagebox.showwarning("Virhe", "Avaa tai luo projekti ensin!")
            return

        file_to_add = filedialog.askopenfilename(title="Valitse projektiin lisättävä tiedosto")
        if file_to_add:
            # Muutetaan polku suhteelliseksi projektitiedostoon nähden
            rel_path = os.path.relpath(file_to_add, os.path.dirname(os.path.abspath(project_path)))
            rel_path = rel_path.replace("\\", "/") # CodeBlocks käyttää vinoviivoja

            try:
                tree = ET.parse(project_path)
                root = tree.getroot()
                proj_node = root.find("Project")

                # Tarkistetaan, onko tiedosto jo projektissa
                already_exists = False
                for unit in proj_node.findall("Unit"):
                    if unit.get("filename") == rel_path:
                        already_exists = True
                        break

                if not already_exists:
                    new_unit = ET.SubElement(proj_node, "Unit")
                    new_unit.set("filename", rel_path)
                    
                    # Tallennetaan kauniisti sisennettynä
                    self._indent_xml(root)
                    tree.write(project_path, encoding="UTF-8", xml_declaration=True)
                    
                    self.load_cbp_project(project_path) # Päivitetään puu
                    self.update_status(f"Lisätty: {rel_path}")
                else:
                    messagebox.showinfo("Huomio", "Tiedosto on jo projektissa.")

            except Exception as e:
                messagebox.showerror("Virhe", f"Tiedoston lisäys epäonnistui: {e}")

    def _indent_xml(self, elem, level=0):
        """Apumetodi XML:n siistiin sisentämiseen."""
        i = "\n" + level*"\t"
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "\t"
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self._indent_xml(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
	
    def load_last_project(self):
        """Lataa viimeksi auki olleen projektin asetuksista."""
        last_proj = self.settings.get("current_project")
        if last_proj and os.path.exists(last_proj):
            self.load_cbp_project(last_proj)

    def load_cbp_project(self, filename):
        """Lataa Code::Blocks-projektin ja päivittää puunäkymän."""
        if not filename: return
        
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            proj_node = root.find("Project")
            
            if proj_node is not None:
                # Tyhjennetään nykyinen puu
                for i in self.project_tree.get_children():
                    self.project_tree.delete(i)
                
                title = "Bittinikkari"
                # Haetaan nimi <Option title="..."/> tagista
                for opt in proj_node.findall("Option"):
                    if opt.get("title"):
                        title = opt.get("title")
                
                # Tallennetaan polku asetuksiin
                self.settings["current_project"] = filename
                
                # Rakennetaan puu (kuten aiemmin määriteltiin)
                main_node = self.project_tree.insert("", "end", text=title, open=True, values=(filename,))
                
                # Täytetään tiedostot <Unit filename="..."/> tageista
                for unit in proj_node.findall("Unit"):
                    f_name = unit.get("filename")
                    self.project_tree.insert(main_node, "end", text=f_name, values=(f_name,))
                
                self.update_status(f"Projekti ladattu: {os.path.basename(filename)}")
        except Exception as e:
            messagebox.showerror("Luku-virhe", f"CBP-tiedostoa ei voitu lukea: {e}")




