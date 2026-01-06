import os
import sys
import platform

def create_windows_shortcut(name, path):
    """Creates a Windows shortcut and attaches an icon if available."""
    try:
        import winshell
        from win32com.client import Dispatch
    except ImportError:
        print(f"❌ Error: Required libraries (winshell/pywin32) missing for {name}.")
        return False

    desktop = winshell.desktop()
    lnk_path = os.path.join(desktop, f"{name}.lnk")
    
    # Using pythonw.exe to prevent the black console window from appearing
    pythonw_exe = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
    
    # Looks for 'icon.ico' in the same folder as the script
    icon_path = os.path.join(os.path.dirname(path), "icon.ico")
    
    try:
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(lnk_path)
        shortcut.Targetpath = pythonw_exe
        shortcut.Arguments = f'"{path}"'
        shortcut.WorkingDirectory = os.path.dirname(path)
        shortcut.Description = f"{name} Code Editor"
        
        # Apply the icon if it exists
        if os.path.exists(icon_path):
            shortcut.IconLocation = icon_path
            icon_status = "with custom icon"
        else:
            icon_status = "without icon"
            
        shortcut.save()
        print(f"✅ Windows shortcut created {icon_status}: {name}")
        return True
    except Exception as e:
        print(f"❌ Windows system error: {e}")
        return False

def find_version_files():
    """Scans the current directory for Bittinikkari script files."""
    found = {}
    current_dir = os.getcwd()
    
    # Dictionary mapping display names to the actual filenames
    targets = {
        "Bittinikkari Lite": "bittinikkari-lite.py",
        "Bittinikkari Medium": "bittinikkari-medium.py"
    }
    
    for label, filename in targets.items():
        full_path = os.path.join(current_dir, filename)
        if os.path.exists(full_path):
            found[label] = full_path
        else:
            print(f"⚠️ File not found in this folder: {filename}")
            
    return found

if __name__ == "__main__":
    print("--- Bittinikkari Installer ---")
    system = platform.system()
    files_to_install = find_version_files()
    
    if not files_to_install:
        print("❌ No Bittinikkari files found. Please run this script in the correct folder.")
        sys.exit()

    if system == "Windows":
        # Check for necessary Windows-specific libraries
        try:
            import winshell
        except ImportError:
            print("\nREQUIRED: Please install libraries first:")
            print("pip install winshell pywin32")
            sys.exit()

    # Process each found version
    for name, path in files_to_install.items():
        if system == "Windows":
            create_windows_shortcut(name, path)
        # Note: Linux shortcut logic can be added here if needed later

    print("\nInstallation process finished.")