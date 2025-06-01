# import webview
# import os
# import threading
# from flask import Flask, render_template_string, send_from_directory, request, jsonify
# from pathlib import Path
# from tkinter import Tk, filedialog
# import shutil
# import datetime
# import re
# import sys 

# app = Flask(__name__, static_folder='app')
# DEBUG = True
# PORT = 5000
# HOST = '127.0.0.1'

# FILE_TYPE_MAP = {
#     "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".heic"],
#     "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
#     "Audio": [".mp3", ".wav", ".aac", ".ogg", ".flac"],
#     "Videos": [".mp4", ".avi", ".mkv", ".mov"],
#     "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
#     "Executables": [".exe", ".msi", ".apk", ".bat"],
#     "Programming": [
#         ".py", ".java", ".cpp", ".c", ".cs", ".js", ".ts", ".jsx", ".tsx", ".html", ".css",
#         ".php", ".rb", ".go", ".rs", ".swift", ".kt", ".m", ".scala", ".pl", ".sh", ".bat",
#         ".ps1", ".vb", ".lua", ".sql", ".erl", ".ex", ".exs", ".groovy", ".coffee", ".dart",
#         ".h", ".hpp", ".r", ".md", ".yaml", ".yml", ".json", ".ini", ".cfg"
#     ]
# }

# @app.route('/')
# def index():
#     html_path = os.path.join(app.static_folder, 'index.html')
#     with open(html_path, 'r', encoding='utf-8') as f:
#         return render_template_string(f.read())

# @app.route('/<path:filename>')
# def static_files(filename):
#     return send_from_directory(app.static_folder, filename)


# @app.route('/undo', methods=['POST'])
# def undo_organization():
#     try:
#         # Assuming log is inside the sorted folder
#         log_path = os.path.join('sorted', 'log.txt')

#         if not os.path.exists(log_path):
#             return jsonify({'message': 'No log file found to undo.'})

#         moved_files = []
#         with open(log_path, 'r') as f:
#             for line in f:
#                 # Skip headers and dividers
#                 if line.startswith("|") and not line.startswith("| File Name"):
#                     parts = [p.strip() for p in line.strip().split('|')[1:-1]]
#                     if len(parts) >= 3:
#                         file_name = parts[0]
#                         source = parts[1]
#                         dest = parts[2]
#                         current_path = os.path.join(dest, file_name)
#                         original_path = os.path.join(source, file_name)

#                         # If renamed, use column 6 (optional: File Name Changed To)
#                         if len(parts) >= 7 and parts[6]:
#                             renamed_file = parts[6]
#                             current_path = os.path.join(dest, renamed_file)

#                         if os.path.exists(current_path):
#                             os.makedirs(os.path.dirname(original_path), exist_ok=True)
#                             shutil.move(current_path, original_path)
#                             moved_files.append(f"Moved back: {file_name}")
        
#         return jsonify({'message': f"Undo complete. {len(moved_files)} file(s) restored.", 'log': '\n'.join(moved_files)})

#     except Exception as e:
#         return jsonify({'message': 'Undo failed.', 'log': str(e)})


# @app.route('/organize', methods=['POST'])
# def organize_files():
#     data = request.get_json()
#     source_folder = data.get('source_folder')
#     destination_folder = data.get('destination_folder') or source_folder
#     include_subfolders = data.get('include_subfolders', False)
#     date_sorting = data.get('date_sorting', False)
#     keywords_input = data.get('keywords', '').strip()
#     filters = data.get('filters', [])

#     if not source_folder or not os.path.isdir(source_folder):
#         return jsonify({'status': 'error', 'message': 'Invalid source folder.'})

#     sorted_folder = os.path.join(destination_folder, "sorted")
#     os.makedirs(sorted_folder, exist_ok=True)
#     log_path = os.path.join(sorted_folder, "log.txt")
#     moved_files = []

#     allowed_exts = set()
#     if "All" in filters or not filters:
#         for exts in FILE_TYPE_MAP.values():
#             allowed_exts.update(exts)
#     else:
#         for f in filters:
#             allowed_exts.update(FILE_TYPE_MAP.get(f, []))

#     all_known_exts = set(sum(FILE_TYPE_MAP.values(), []))
#     programming_exts = set(FILE_TYPE_MAP["Programming"])

#     keyword_list = [kw.strip() for kw in keywords_input.split(',') if kw.strip()]
#     keyword_patterns = [re.compile(re.escape(kw), re.IGNORECASE) for kw in keyword_list]
#     apply_keyword_filtering = bool(keyword_list)

#     file_iterator = os.walk(source_folder) if include_subfolders else [(source_folder, [], os.listdir(source_folder))]

#     for root, _, files in file_iterator:
#         for file in files:
#             full_path = os.path.join(root, file)
#             if not os.path.isfile(full_path):
#                 continue

#             ext = Path(file).suffix.lower()

#             if ext in programming_exts:
#                 continue

#             matched_keyword = ''
#             for pattern, kw in zip(keyword_patterns, keyword_list):
#                 if pattern.search(file):
#                     matched_keyword = kw
#                     break

#             # If keyword filtering is enabled and file doesn't match any keyword, skip it
#             if apply_keyword_filtering and not matched_keyword:
#                 continue

#             # If not matched by keyword and not allowed extension, AND extension is known, skip it
#             if not matched_keyword and ext not in allowed_exts and ext in all_known_exts:
#                 continue

#             file_type = "Miscellaneous"
#             for category, extensions in FILE_TYPE_MAP.items():
#                 if ext in extensions and category != "Programming":
#                     file_type = category
#                     break

#             subfolder_parts = []

#             if matched_keyword:
#                 subfolder_parts.append(matched_keyword.replace(" ", "_"))
#                 if file_type == "Miscellaneous":
#                     subfolder_parts.append("Miscellaneous")
#                 else:
#                     subfolder_parts.append(file_type)
#             else:
#                 subfolder_parts.append(file_type)

#             subcategory = ext[1:] if ext else "others"
#             subfolder_parts.append(subcategory)

#             if date_sorting:
#                 date_str = datetime.datetime.fromtimestamp(os.path.getctime(full_path)).strftime('%Y-%m-%d')
#                 subfolder_parts.append(date_str)
#             else:
#                 date_str = ""

#             dest_dir = os.path.join(sorted_folder, *subfolder_parts)
#             os.makedirs(dest_dir, exist_ok=True)

#             original_file_name = file
#             dest_path = os.path.join(dest_dir, original_file_name)
#             file_name_changed_to = ''

#             if os.path.abspath(full_path) == os.path.abspath(dest_path):
#                 continue

#             counter = 1
#             while os.path.exists(dest_path):
#                 file_base, file_ext = os.path.splitext(original_file_name)
#                 new_name = f"{file_base}_{counter}{file_ext}"
#                 dest_path = os.path.join(dest_dir, new_name)
#                 counter += 1

#             if original_file_name != os.path.basename(dest_path):
#                 file_name_changed_to = os.path.basename(dest_path)

#             shutil.move(full_path, dest_path)

#             moved_files.append({
#                 'file': original_file_name,
#                 'changed': file_name_changed_to,
#                 'source': root,
#                 'dest': dest_dir,
#                 'category': file_type,
#                 'subcategory': subcategory,
#                 'date': date_str,
#                 'keyword': matched_keyword or ''
#             })

#     if moved_files:
#         name_col_width = max(len('File Name'), max((len(f['file']) for f in moved_files), default=0))
#         changed_col_width = max(len('File Name Changed To'), max((len(f['changed']) for f in moved_files), default=0))
#         source_col_width = max(len('Source Folder'), max((len(f['source']) for f in moved_files), default=0))
#         dest_col_width = max(len('Destination Folder'), max((len(f['dest']) for f in moved_files), default=0))
#         category_col_width = max(len('Category'), max((len(f['category']) for f in moved_files), default=0))
#         subcategory_col_width = max(len('Subcategory'), max((len(f['subcategory']) for f in moved_files), default=0))
#         date_col_width = max(len('Date'), max((len(f['date']) for f in moved_files), default=0))
#         keyword_col_width = max(len('Keyword Hit'), max((len(f['keyword']) for f in moved_files), default=0))

#         header = (
#             f"{'File Name':<{name_col_width}} | "
#             f"{'File Name Changed To':<{changed_col_width}} | "
#             f"{'Source Folder':<{source_col_width}} | "
#             f"{'Destination Folder':<{dest_col_width}} | "
#             f"{'Category':<{category_col_width}} | "
#             f"{'Subcategory':<{subcategory_col_width}} | "
#             f"{'Date':<{date_col_width}} | "
#             f"{'Keyword Hit':<{keyword_col_width}}"
#         )
#         separator = '-' * len(header)
#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         centered_time = f"Sorted Date & Time: {timestamp}".center(len(header))

#         with open(log_path, "a", encoding="utf-8") as log_file:
#             log_file.write(f"\n{separator}\n{centered_time}\n{separator}\n")
#             log_file.write(header + "\n")
#             log_file.write(separator + "\n")
#             for f in moved_files:
#                 log_file.write(
#                     f"{f['file']:<{name_col_width}} | "
#                     f"{f['changed']:<{changed_col_width}} | "
#                     f"{f['source']:<{source_col_width}} | "
#                     f"{f['dest']:<{dest_col_width}} | "
#                     f"{f['category']:<{category_col_width}} | "
#                     f"{f['subcategory']:<{subcategory_col_width}} | "
#                     f"{f['date']:<{date_col_width}} | "
#                     f"{f['keyword']:<{keyword_col_width}}\n"
#                 )

#     return jsonify({
#         'status': 'success',
#         'message': f'Organized {len(moved_files)} file(s).',
#         'files': [f['file'] for f in moved_files]
#     })

# class Api:
#     def choose_folder(self):
#         root = Tk()
#         root.withdraw()
#         folder = filedialog.askdirectory()
#         root.destroy()
#         return folder or None

# def run_flask():
#     app.run(host=HOST, port=PORT, debug=DEBUG, use_reloader=False)

# def start_webview():
#     api = Api()
#     window = webview.create_window(
#         'Automated File Organizer',
#         url=f'http://{HOST}:{PORT}',
#         js_api=api,
#         width=800,
#         height=600,
#         min_size=(600, 450),
#         confirm_close=True,
#         text_select=True,
#         background_color='#FFFFFF'
#     )
#     webview.start(debug=DEBUG, http_server=False)

# if __name__ == '__main__':
#     if not os.path.exists(os.path.join(os.getcwd(), 'app')):
#         raise FileNotFoundError("Missing 'app' directory with frontend files.")
#     threading.Thread(target=run_flask, daemon=True).start()
#     start_webview()























import webview
import os
import sys
import threading
from flask import Flask, render_template_string, send_from_directory, request, jsonify
from pathlib import Path
from tkinter import Tk, filedialog
import shutil
import datetime
import re

def get_resource_path(relative_path):
    try:
        # PyInstaller temp folder
        base_path = sys._MEIPASS
    except AttributeError:
        # When running directly
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

STATIC_FOLDER = get_resource_path("app")
app = Flask(__name__, static_folder=STATIC_FOLDER)

DEBUG = True
PORT = 5000
HOST = '127.0.0.1'

FILE_TYPE_MAP = {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".heic"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Audio": [".mp3", ".wav", ".aac", ".ogg", ".flac"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executables": [".exe", ".msi", ".apk", ".bat"],
    "Programming": [
        ".py", ".java", ".cpp", ".c", ".cs", ".js", ".ts", ".jsx", ".tsx", ".html", ".css",
        ".php", ".rb", ".go", ".rs", ".swift", ".kt", ".m", ".scala", ".pl", ".sh", ".bat",
        ".ps1", ".vb", ".lua", ".sql", ".erl", ".ex", ".exs", ".groovy", ".coffee", ".dart",
        ".h", ".hpp", ".r", ".md", ".yaml", ".yml", ".json", ".ini", ".cfg"
    ]
}

@app.route('/')
def index():
    html_path = os.path.join(STATIC_FOLDER, 'index.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        return render_template_string(f.read())

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(STATIC_FOLDER, filename)

@app.route('/undo', methods=['POST'])
def undo_organization():
    try:
        log_path = os.path.join('sorted', 'log.txt')
        if not os.path.exists(log_path):
            return jsonify({'message': 'No log file found to undo.'})

        moved_files = []
        with open(log_path, 'r') as f:
            for line in f:
                if line.startswith("|") and not line.startswith("| File Name"):
                    parts = [p.strip() for p in line.strip().split('|')[1:-1]]
                    if len(parts) >= 3:
                        file_name, source, dest = parts[0], parts[1], parts[2]
                        current_path = os.path.join(dest, file_name)
                        original_path = os.path.join(source, file_name)

                        if len(parts) >= 7 and parts[6]:
                            renamed_file = parts[6]
                            current_path = os.path.join(dest, renamed_file)

                        if os.path.exists(current_path):
                            os.makedirs(os.path.dirname(original_path), exist_ok=True)
                            shutil.move(current_path, original_path)
                            moved_files.append(f"Moved back: {file_name}")

        return jsonify({'message': f"Undo complete. {len(moved_files)} file(s) restored.", 'log': '\n'.join(moved_files)})

    except Exception as e:
        return jsonify({'message': 'Undo failed.', 'log': str(e)})

@app.route('/organize', methods=['POST'])
def organize_files():
    data = request.get_json()
    source_folder = data.get('source_folder')
    destination_folder = data.get('destination_folder') or source_folder
    include_subfolders = data.get('include_subfolders', False)
    date_sorting = data.get('date_sorting', False)
    keywords_input = data.get('keywords', '').strip()
    filters = data.get('filters', [])

    if not source_folder or not os.path.isdir(source_folder):
        return jsonify({'status': 'error', 'message': 'Invalid source folder.'})

    sorted_folder = os.path.join(destination_folder, "sorted")
    os.makedirs(sorted_folder, exist_ok=True)
    log_path = os.path.join(sorted_folder, "log.txt")
    moved_files = []

    allowed_exts = set()
    if "All" in filters or not filters:
        for exts in FILE_TYPE_MAP.values():
            allowed_exts.update(exts)
    else:
        for f in filters:
            allowed_exts.update(FILE_TYPE_MAP.get(f, []))

    all_known_exts = set(sum(FILE_TYPE_MAP.values(), []))
    programming_exts = set(FILE_TYPE_MAP["Programming"])

    keyword_list = [kw.strip() for kw in keywords_input.split(',') if kw.strip()]
    keyword_patterns = [re.compile(re.escape(kw), re.IGNORECASE) for kw in keyword_list]
    apply_keyword_filtering = bool(keyword_list)

    file_iterator = os.walk(source_folder) if include_subfolders else [(source_folder, [], os.listdir(source_folder))]

    for root, _, files in file_iterator:
        for file in files:
            full_path = os.path.join(root, file)
            if not os.path.isfile(full_path):
                continue

            ext = Path(file).suffix.lower()
            if ext in programming_exts:
                continue

            matched_keyword = ''
            for pattern, kw in zip(keyword_patterns, keyword_list):
                if pattern.search(file):
                    matched_keyword = kw
                    break

            if apply_keyword_filtering and not matched_keyword:
                continue

            if not matched_keyword and ext not in allowed_exts and ext in all_known_exts:
                continue

            file_type = "Miscellaneous"
            for category, extensions in FILE_TYPE_MAP.items():
                if ext in extensions and category != "Programming":
                    file_type = category
                    break

            subfolder_parts = []

            if matched_keyword:
                subfolder_parts.append(matched_keyword.replace(" ", "_"))
                if file_type == "Miscellaneous":
                    subfolder_parts.append("Miscellaneous")
                else:
                    subfolder_parts.append(file_type)
            else:
                subfolder_parts.append(file_type)

            subcategory = ext[1:] if ext else "others"
            subfolder_parts.append(subcategory)

            if date_sorting:
                date_str = datetime.datetime.fromtimestamp(os.path.getctime(full_path)).strftime('%Y-%m-%d')
                subfolder_parts.append(date_str)
            else:
                date_str = ""

            dest_dir = os.path.join(sorted_folder, *subfolder_parts)
            os.makedirs(dest_dir, exist_ok=True)

            original_file_name = file
            dest_path = os.path.join(dest_dir, original_file_name)
            file_name_changed_to = ''

            if os.path.abspath(full_path) == os.path.abspath(dest_path):
                continue

            counter = 1
            while os.path.exists(dest_path):
                file_base, file_ext = os.path.splitext(original_file_name)
                new_name = f"{file_base}_{counter}{file_ext}"
                dest_path = os.path.join(dest_dir, new_name)
                counter += 1

            if original_file_name != os.path.basename(dest_path):
                file_name_changed_to = os.path.basename(dest_path)

            shutil.move(full_path, dest_path)

            moved_files.append({
                'file': original_file_name,
                'changed': file_name_changed_to,
                'source': root,
                'dest': dest_dir,
                'category': file_type,
                'subcategory': subcategory,
                'date': date_str,
                'keyword': matched_keyword or ''
            })

    if moved_files:
        name_col_width = max(len('File Name'), max((len(f['file']) for f in moved_files), default=0))
        changed_col_width = max(len('File Name Changed To'), max((len(f['changed']) for f in moved_files), default=0))
        source_col_width = max(len('Source Folder'), max((len(f['source']) for f in moved_files), default=0))
        dest_col_width = max(len('Destination Folder'), max((len(f['dest']) for f in moved_files), default=0))
        category_col_width = max(len('Category'), max((len(f['category']) for f in moved_files), default=0))
        subcategory_col_width = max(len('Subcategory'), max((len(f['subcategory']) for f in moved_files), default=0))
        date_col_width = max(len('Date'), max((len(f['date']) for f in moved_files), default=0))
        keyword_col_width = max(len('Keyword Hit'), max((len(f['keyword']) for f in moved_files), default=0))

        header = (
            f"{'File Name':<{name_col_width}} | "
            f"{'File Name Changed To':<{changed_col_width}} | "
            f"{'Source Folder':<{source_col_width}} | "
            f"{'Destination Folder':<{dest_col_width}} | "
            f"{'Category':<{category_col_width}} | "
            f"{'Subcategory':<{subcategory_col_width}} | "
            f"{'Date':<{date_col_width}} | "
            f"{'Keyword Hit':<{keyword_col_width}}"
        )
        separator = '-' * len(header)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        centered_time = f"Sorted Date & Time: {timestamp}".center(len(header))

        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"\n{separator}\n{centered_time}\n{separator}\n")
            log_file.write(header + "\n")
            log_file.write(separator + "\n")
            for f in moved_files:
                log_file.write(
                    f"{f['file']:<{name_col_width}} | "
                    f"{f['changed']:<{changed_col_width}} | "
                    f"{f['source']:<{source_col_width}} | "
                    f"{f['dest']:<{dest_col_width}} | "
                    f"{f['category']:<{category_col_width}} | "
                    f"{f['subcategory']:<{subcategory_col_width}} | "
                    f"{f['date']:<{date_col_width}} | "
                    f"{f['keyword']:<{keyword_col_width}}\n"
                )

    return jsonify({
        'status': 'success',
        'message': f'Organized {len(moved_files)} file(s).',
        'files': [f['file'] for f in moved_files]
    })

class Api:
    def choose_folder(self):
        root = Tk()
        root.withdraw()
        folder = filedialog.askdirectory()
        root.destroy()
        return folder or None

def run_flask():
    app.run(host=HOST, port=PORT, debug=DEBUG, use_reloader=False)

def start_webview():
    api = Api()
    window = webview.create_window(
        'Automated File Organizer',
        url=f'http://{HOST}:{PORT}',
        js_api=api,
        width=800,
        height=600,
        min_size=(600, 450),
        confirm_close=True,
        text_select=True,
        background_color='#FFFFFF'
    )
    # webview.start(debug=DEBUG, http_server=False)
    webview.start(debug=False, http_server=False)
    
if __name__ == '__main__':
    if not os.path.exists(STATIC_FOLDER):
        raise FileNotFoundError("Missing 'app' directory with frontend files.")
    threading.Thread(target=run_flask, daemon=True).start()
    start_webview()
