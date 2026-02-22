import subprocess
import sys
import os
import shutil

def build():
    print("--- Hotel Management System Build Script ---")
    
    # Check for pyinstaller
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Build command
    # --onefile: Create a single executable
    # --noconsole: Hide terminal window
    # --add-data: Include UI folder and initial database
    # Note: On Windows, use ; as separator, on Linux/Mac use :
    sep = ';' if os.name == 'nt' else ':'
    
    cmd = [
        "pyinstaller",
        "--noconsole",
        "--onefile",
        f"--add-data=ui{sep}ui",
        f"--add-data=hotel.db{sep}.",
        "--name=HotelManagement",
        "main.py"
    ]

    print(f"Running command: {' '.join(cmd)}")
    subprocess.call(cmd)

    print("\n--- Build Finished ---")
    print("Your executable is in the 'dist' folder.")
    print("To create a 'Next-Next' Setup Installer, please follow the steps in DISTRIBUTION.md")

if __name__ == "__main__":
    build()
