# Bittinikkari - bittinikkari-medium.py 
# Tekijä: Tuomas Lähteenmäki
# Version 0.2 
# Lisenssi: GNU GPLv3
import sys
import os

# Lisätään modules-kansio polkuun
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

try:
    from editor_ui import BittinikkariEditor
    import tkinter as tk

    def main():
        root = tk.Tk()
        app = BittinikkariEditor(root)
        root.mainloop()

    if __name__ == "__main__":
        main()
except ImportError as e:
    print(f"Virhe moduulien latauksessa: {e}")

    print("Varmista, että 'modules'-kansiossa on __init__.py ja editor_ui.py.")

