# Grand Hotel Management System

A professional, modern desktop application for managing small to medium-sized hotels. Built with Python Tkinter and SQLite.

## Features
- **Modern Dashboard**: Real-time stats and smooth navigation.
- **Room Management**: Visual grid with status-based coloring.
- **Booking System**: Easy check-in/out and automated cost calculation.
- **Guest Management**: Searchable database of all customers.
- **Professional Branding**: Clean dark-themed UI with custom rounded widgets.
- **Billing & Invoicing**: Automated invoice generation.

---

## Installation & Usage

### 🐧 Linux (Ubuntu/Debian)
Use the provided launcher script for automatic setup:
1.  Open Terminal in the project folder.
2.  Give execution permission:
    ```bash
    chmod +x run_linux.sh
    ```
3.  Run the app:
    ```bash
    ./run_linux.sh
    ```
    *(To run in background so it keeps running after you close the terminal: `./run_linux.sh -d`)*

### 🪟 Windows
1.  Install **Python 3.10+** from [python.org](https://www.python.org/).
2.  Open Command Prompt (CMD) in the project folder.
3.  Install dependencies:
    ```cmd
    pip install -r requirements.txt
    ```
4.  Run the app:
    ```cmd
    python main.py
    ```

### 🍎 macOS
1.  Install Python via [Homebrew](https://brew.sh/) or Python.org.
2.  Ensure `tkinter` is installed (usually comes with Python on Mac, if not: `brew install python-tk`).
3.  Open Terminal in the project folder.
4.  Install dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```
5.  Run the app:
    ```bash
    python3 main.py
    ```

---

## Packaging for Distribution
If you want to create a single `.exe` or `.app` file:
1.  See [DISTRIBUTION.md](DISTRIBUTION.md) for detailed instructions.
2.  Run the build script:
    ```bash
    python build_exe.py
    ```

## Credits
Built by **Sakib Al Hasan** & **Antigravity AI**.
© 2026 Grand Hotel Management System
