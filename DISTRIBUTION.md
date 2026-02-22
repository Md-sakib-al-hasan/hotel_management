# Hotel Management System - Distribution Guide (Next-Next Installer)

To give your users a professional experience where they can download a setup file and click "Next, Next, Finish", follow these steps.

## Step 1: Create the Executable (.exe)
First, you need to turn your Python code into a single file.

1.  Open your terminal/command prompt.
2.  Run the build script I created for you:
    ```bash
    python build_exe.py
    ```
3.  Once finished, look for a folder named `dist`. Inside, you will find `HotelManagement.exe` (or just `HotelManagement` on Linux).

> [!IMPORTANT]
> To create a Windows `.exe`, you must run this command on a **Windows** computer.

---

## Step 2: Create the Setup Wizard (Inno Setup)
To create the "Next-Next" installer, we recommend **Inno Setup** (Free).

1.  **Download & Install Inno Setup**: [jrsoftware.org](https://jrsoftware.org/isdl.php)
2.  **Open Inno Setup Compiler** and select "Create a new script file using the Script Wizard".
3.  **App Information**: Enter "Grand Hotel Management System" and your version.
4.  **Application Files**: 
    - For "Application main executable file", select the `HotelManagement.exe` from your `dist` folder.
5.  **Icons**: Check the boxes to "Allow user to create a desktop shortcut".
6.  **Compile**: Click "Finish" and let it compile.

**Result**: You will get a `mysetup.exe` file. This is the only file you need to send to your users!

---

## Step 3: What to send to your users?
Just send the `mysetup.exe` (or whatever you named your installer). 

When the user runs it:
1.  It will ask where to install.
2.  It will copy all files.
3.  It will create a **Desktop Icon**.
4.  They just double-click the icon to start managing their hotel! ✅

---

## Troubleshooting
- **Database issues**: If the app can't find the database after install, make sure you used the `--add-data` flag as handled in `build_exe.py`.
- **Anti-virus**: Since your app is new, Windows might show a "SmartScreen" warning. Users just need to click "More info" -> "Run anyway".
