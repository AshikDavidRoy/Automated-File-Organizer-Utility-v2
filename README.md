# 🗂️ Automated-File-Organizer-Utility-v2

A desktop application built with **Python**, **Flask**, and **pywebview** that helps you organize your files automatically based on type, extension, keyword matches, and creation date. The application offers a clean graphical interface, requires no technical experience, and can be compiled into a single `.exe` file that runs independently on Windows—no Python installation required.

---

## ✅ Features

- 📁 Organizes files by type (Images, Documents, Audio, Video, etc.)
- 🔍 Keyword-based filtering and categorization
- 🗓️ Date-based sorting (optional)
- 🧠 Smart handling of duplicate filenames
- 🧰 GUI built with HTML/CSS and rendered via pywebview
- 📦 Converts into a standalone Windows `.exe`
- 🧊 Embeds static frontend files (HTML, JS, CSS) into the executable
- 🖼️ Custom icon support for the final `.exe`

---

## 🖼️ Preview

Below is a screenshot of the application's user interface:

![App Preview](https://github.com/user-attachments/assets/32e74c8f-76ed-45af-b2e0-967f002e49c7) <sub>*Preview of the File Organizer GUI rendered with pywebview*</sub>

### 🔍 Interface Components Explained

| Component                        | Description                                                                 |
| -------------------------------- | --------------------------------------------------------------------------- |
| **📁 Select Folder** Button      | Opens a native folder picker (via Tkinter) to choose the directory to scan. |
| **Include Subfolders** Checkbox  | When checked, files inside nested directories will also be considered.      |
| **Filter by File Type** Dropdown | Allows the user to limit organizing to specific file types (e.g., Images).  |
| **Keyword Filter** Text Input    | Accepts comma-separated keywords to only move files whose names match them. |
| **Date-Based Sorting** Toggle    | When enabled, organizes files by their creation or modification date.       |
| **Organize** Button              | Starts the file organization process based on selected settings.            |
| **Status Panel / Log Output**    | Displays messages about progress, success, errors, and undo history.        |


---

## 🧰 Tech Stack

| Layer        | Technology             |
|--------------|------------------------|
| Backend      | Python, Flask          |
| Frontend     | HTML, CSS, JavaScript  |
| GUI Wrapper  | pywebview              |
| Packaging    | PyInstaller            |
| File Dialog  | Tkinter (for folder picking) |

---

## 🧱 Project Structure

```

Automated File Organizer Utility/
├── app/               # Frontend (HTML, CSS, JS)
│   ├── index.html
│   ├── style.css
│   └── script.js
├── icon.ico           # Icon for the executable
├── main.py            # Python script (Flask + pywebview)
├── main.spec          # PyInstaller configuration file
└── README.md

````

---

## ⚙️ How It Works

1. A local Flask server runs on `http://127.0.0.1:5000`.
2. pywebview opens a native desktop window pointing to that local address.
3. The frontend UI (in `app/index.html`) is rendered inside the native window.
4. File organizing logic is handled in Python:
   - Files are categorized based on extension/type.
   - Optional filters: subfolder inclusion, keyword matching, date sorting.
   - A `sorted` folder is created with structured subfolders.

---

## 💻 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Clone the Repository

```bash
git[ clone https://github.com/yourusername/automated-file-organizer.git](https://github.com/AshikDavidRoy/Automated-File-Organizer-Utility-v2.git)
cd Automated-File-Organizer-Utility-v2
````

### Install Dependencies

```bash
pip install -r requirements.txt
```

> Example `requirements.txt`:

```
Flask
pywebview
```

---

## 🚀 Usage

### Development Mode

```bash
python main.py
```

1. A window will open.
2. Choose the folder you want to organize.
3. Set filters:

   * File types
   * Include subfolders
   * Keyword filters (comma-separated)
   * Enable/disable date sorting
4. Click **Organize** to begin.

---

## 📦 Packaging Into .EXE

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Generate a `.spec` File

```bash
pyi-makespec --windowed --icon=icon.ico main.py
```

### Step 3: Modify the `.spec` File

Edit the generated `main.spec`:

```python
a = Analysis(
    ...
    datas=[('app', 'app')],  # Include frontend directory
    ...
)
```


### 🛠 Step 4: Build the Executable `.exe` with PyInstaller

Run this command in your terminal (from your project folder):

```bash
pyinstaller main.py --name FileOrganizer --onefile --windowed --icon=icon.ico --add-data "app;app"
```

> **Explanation**:

* `--name FileOrganizer` → Name of output `.exe`
* `--onefile` → Single `.exe`
* `--windowed` → Hides console window
* `--icon=icon.ico` → App icon
* `--add-data "app;app"` → Bundle `app/` folder

---

After build:

```
dist/
└── FileOrganizer/
    ├── FileOrganizer.exe
    ├── app/
    ├── other runtime files
```

### Step 5: Run the `.exe`

Double-click `FileOrganizer.exe` inside the `dist/FileOrganizer/` directory.

✅ Your app will run independently—no Python installation required!

---

## 🛠️ Troubleshooting

### Problem: "Missing app/ directory"

Make sure the `app/` folder with `index.html`, `style.css`, and `script.js` exists and is correctly referenced in both:

* `main.py`
* `main.spec` (`datas=[('app', 'app')]`)

### Problem: pywebview window is blank

Ensure Flask is running and `url=f'http://127.0.0.1:5000'` is correct.

### Problem: `.exe` runs but closes immediately

Run the `.exe` from a terminal to see error messages:

```bash
cd dist/FileOrganizer
./FileOrganizer.exe
```

### Problem: Application icon not showing

Ensure the `.ico` file is:

* In the root folder
* Provided via `--icon=icon.ico` when building with `pyi-makespec`

---

## 🤝 Contributing

Contributions are welcome! Please feel free to:

* Submit pull requests
* Open issues for bugs or feature suggestions
* Fork the project and improve it
