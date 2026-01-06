# Bittinikkari Lite ⚡

**Bittinikkari Lite** is a high-performance, minimalist code editor designed for quick edits and standalone use. Built entirely on Python’s standard Tkinter library, it offers a "zero-dependency" experience, meaning it runs instantly on any system with Python installed without requiring additional library setups.


## Key Features
* **Zero-Dependency:** Runs on standard Python libraries. No `pip install` required for the editor itself.
* **Minimalist UI:** Clean, dark-themed interface optimized for readability.
* **Safety First:** Automatically creates a `.bak` backup file before every save to prevent data loss.
* **One-Click Optimizer:** Built-in tool to remove trailing whitespaces and clean up code formatting.
* **Custom Branding:** Includes support for a custom `icon.ico` for a professional desktop experience.


## Installation & Setup

### 1. Basic Usage
Simply run the script with Python:
```bash
python bittinikkari-lite.py
```

### 🚀 Installation

1. **Prerequisites:**
   * Python 3.12 or newer.
   * (Windows Only) For automated shortcut creation: `pip install winshell pywin32`.

2. **Automatic Desktop Setup:**
   Run the included installer to create cross-platform shortcuts:
   ```bash
   python install_bittinikkari.py

---

## Project Structure
bittinikkari-lite.py: The main editor script.
   * ```icon.ico```: The application icon.
   * ```install_bittinikkari.py```: Shortcut creator for Windows and Linux environments.

   
## Version History
   * v0.1: Initial release, basic file operations.
   * v0.2: Added English documentation, icon support, and whitespace optimization.

## License & Credits
   * Author: Tuomas Lähteenmäki
   * License: GNU GPLv3 - Free to use, modify, and distribute.
---
Developed for the flow of coding.
