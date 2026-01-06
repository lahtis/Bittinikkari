# Bittinikkari Editor

Bittinikkari is a specialized, open-source code editor designed for Python and C development. It focuses on lightweight performance, project management, and smart code maintenance.

### 2. Bittinikkari Lite (`bittinikkari_lite.py`)
A minimalist, "standalone" editor for quick edits.
* **Zero Dependencies:** All logic contained within a single file.
* **Dark Mode:** A clean, dark-themed editor for focus.
* **Speed:** Instant startup, ideal for emergency edits or single-script tweaks.

---

## ✨ Key Features

* **Automatic Backups:** Every save operation automatically generates a `.bak` backup file to prevent data loss.
* **C Memory Safety:** Built-in analyzer that scans code for `malloc` calls and warns if a corresponding `free` is missing.
* **One-Command Optimization (⚡):** Use the Lightning button or `Ctrl+Shift+B` to perform a "Mass Cleanup":
    * Auto-indentation correction.
    * Removal of trailing whitespace.
    * Instant project-wide backup.
* **Native Performance:** Built entirely on Python's standard library (**Tkinter**), requiring no external `pip` installations for the editor itself.

---

## 🚀 Installation & Setup

1. **Prerequisites:**
   * Python 3.12 or newer.
   * (Windows Only) For automated shortcut creation: `pip install winshell pywin32`.

2. **Automatic Desktop Setup:**
   Run the included installer to create cross-platform shortcuts:
   ```bash
   python install_bittinikkari.py

