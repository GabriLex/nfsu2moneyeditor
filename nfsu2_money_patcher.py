import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import struct
import os
import sys
import shutil
import ctypes

# --- GESTIONE PERMESSI AMMINISTRATORE ---
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

run_as_admin()

# --- CONFIGURAZIONE E TRADUZIONI ---
LANG = {
    'IT': {
        'title': 'NFSU2 Money Patcher',
        'credits_label': 'CREDITI DA AGGIUNGERE',
        'limits_label': '(Min: 50 - Max: 999,999,999)',
        'extract_button': 'ESTRAI SALVATAGGI',
        'patch_button': 'PATCHA SALVATAGGI',
        'restore_button': 'RIPRISTINA ORIGINALI',
        'footer': 'Need for Speed Underground 2 - Money Editor',
        'signature': 'GabriLex vers. 1.0.0',
        'error': 'Errore',
        'success': 'Successo',
        'warning': 'Attenzione',
        'info': 'Informazione',
        'invalid_number': 'Inserisci un numero valido.',
        'out_of_range': 'Valore fuori limite (50 - 999,999,999).',
        'auto_detected': 'Salvataggi rilevati!\n\nCartella:\n{0}\n\nFile trovati: {1}',
        'auto_detect_failed': 'Salvataggi non trovati automaticamente.\nSeleziona la cartella manualmente.',
        'saves_extracted': 'Backup creato sul Desktop!\n{0} file copiati.',
        'saves_patched': 'Patch applicata!\n{0} file modificati con {1} crediti.',
        'saves_restored': 'Originali ripristinati!\n{0} file sovrascritti.',
        'image_not_found': '[ File mancante ]',
        'select_folder': 'Seleziona cartella salvataggi NFSU2'
    },
    'EN': {
        'title': 'NFSU2 Money Patcher',
        'credits_label': 'CREDITS TO ADD',
        'limits_label': '(Min: 50 - Max: 999,999,999)',
        'extract_button': 'EXTRACT SAVES',
        'patch_button': 'PATCH SAVES',
        'restore_button': 'RESTORE ORIGINALS',
        'footer': 'Need for Speed Underground 2 - Money Editor',
        'signature': 'GabriLex vers. 1.0.0',
        'error': 'Error',
        'success': 'Success',
        'warning': 'Warning',
        'info': 'Information',
        'invalid_number': 'Please enter a valid number.',
        'out_of_range': 'Value out of range (50 - 999,999,999).',
        'auto_detected': 'Saves detected!\n\nFolder:\n{0}\n\nFiles found: {1}',
        'auto_detect_failed': 'Saves not found automatically.\nPlease select folder manually.',
        'saves_extracted': 'Backup created on Desktop!\n{0} files copied.',
        'saves_patched': 'Patch applied!\n{0} files modified with {1} credits.',
        'saves_restored': 'Originals restored!\n{0} files overwritten.',
        'image_not_found': '[ Missing file ]',
        'select_folder': 'Select NFSU2 save folder'
    }
}

MIN_CREDITS = 50
MAX_CREDITS = 999999999
BACKUP_FOLDER_NAME = "ORIGINALSAVEGAMES"
current_lang = 'IT'

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_backup_folder():
    return os.path.join(os.path.expanduser("~"), 'Desktop', BACKUP_FOLDER_NAME)

def find_save_files_recursive(directory):
    save_files = []
    if not os.path.exists(directory): return []
    for root_dir, _, files in os.walk(directory):
        folder_name = os.path.basename(root_dir)
        for file in files:
            if file == folder_name:
                save_files.append(os.path.join(root_dir, file))
    return save_files

def auto_detect_save_folder():
    local_app_data = os.environ.get('LOCALAPPDATA', '')
    search_paths = [
        os.path.join(local_app_data, 'NFS Underground 2'),
        os.path.join(os.environ.get('USERPROFILE', ''), 'Local Settings', 'Application Data', 'NFS Underground 2'),
        os.path.join(local_app_data, 'VirtualStore', 'Program Files (x86)', 'EA GAMES', 'NFS Underground 2')
    ]
    for path in search_paths:
        if os.path.exists(path):
            files = find_save_files_recursive(path)
            if files: return path, files
    return None, []

# --- LOGICA BOTTONI ---
def extract_saves():
    nfs_folder, save_files = auto_detect_save_folder()
    if not nfs_folder:
        nfs_folder = filedialog.askdirectory(title=LANG[current_lang]['select_folder'])
        if not nfs_folder: return
        save_files = find_save_files_recursive(nfs_folder)
    if not save_files: return
    backup_root = get_backup_folder()
    for f in save_files:
        profile_name = os.path.basename(f)
        dest_dir = os.path.join(backup_root, profile_name)
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy2(f, os.path.join(dest_dir, profile_name))
    messagebox.showinfo(LANG[current_lang]['success'], LANG[current_lang]['saves_extracted'].format(len(save_files)))

def patch_saves():
    try:
        new_money = int(money_entry.get())
        if not (MIN_CREDITS <= new_money <= MAX_CREDITS): raise ValueError
    except ValueError:
        messagebox.showerror(LANG[current_lang]['error'], LANG[current_lang]['out_of_range'])
        return
    _, save_files = auto_detect_save_folder()
    if not save_files:
        folder = filedialog.askdirectory()
        if not folder: return
        save_files = find_save_files_recursive(folder)
    patched = 0
    for file_path in save_files:
        with open(file_path, "rb") as f:
            data = bytearray(f.read())
        if len(data) > 41326:
            data[41322:41326] = struct.pack("<I", new_money)
            with open(file_path, "wb") as f:
                f.write(data)
            patched += 1
    messagebox.showinfo(LANG[current_lang]['success'], LANG[current_lang]['saves_patched'].format(patched, f"{new_money:,}"))

def restore_saves():
    backup_root = get_backup_folder()
    if not os.path.exists(backup_root): return
    target_root, _ = auto_detect_save_folder()
    if not target_root:
        target_root = filedialog.askdirectory()
        if not target_root: return
    restored = 0
    backup_files = find_save_files_recursive(backup_root)
    for b_file in backup_files:
        profile = os.path.basename(b_file)
        dest = os.path.join(target_root, profile, profile)
        if os.path.exists(os.path.dirname(dest)):
            shutil.copy2(b_file, dest)
            restored += 1
    messagebox.showinfo(LANG[current_lang]['success'], LANG[current_lang]['saves_restored'].format(restored))

# --- INTERFACCIA GRAFICA ---
root = tk.Tk()
root.title("NFSU2 Money Patcher")
root.geometry("400x620") # Leggermente più alta per la firma
root.configure(bg="#121212")

# IMPOSTAZIONE ICONA (.ico)
try:
    icon_path = resource_path("nfsu2_icon.ico")
    root.iconbitmap(icon_path)
except Exception as e:
    print(f"Errore caricamento icona: {e}")

def change_language(event=None):
    global current_lang
    current_lang = lang_var.get()
    root.title(LANG[current_lang]['title'])
    credits_label.config(text=LANG[current_lang]['credits_label'])
    limits_label.config(text=LANG[current_lang]['limits_label'])
    btn_extract.config(text=LANG[current_lang]['extract_button'])
    btn_patch.config(text=LANG[current_lang]['patch_button'])
    btn_restore.config(text=LANG[current_lang]['restore_button'])
    footer_label.config(text=LANG[current_lang]['footer'])
    signature_label.config(text=LANG[current_lang]['signature'])

# Header Image
try:
    img_path = resource_path("nfs.jpg")
    pil_img = Image.open(img_path)
    pil_img = pil_img.resize((380, 200), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(pil_img)
    tk.Label(root, image=img, bg="#121212").pack(pady=10)
except:
    tk.Label(root, text="NFSU2 PATCHER", fg="white", bg="#121212", font=("Arial", 20)).pack(pady=20)

lang_var = tk.StringVar(value='IT')
lang_cb = ttk.Combobox(root, textvariable=lang_var, values=['IT', 'EN'], state="readonly", width=5)
lang_cb.pack(anchor="ne", padx=10)
lang_cb.bind("<<ComboboxSelected>>", change_language)

credits_label = tk.Label(root, text=LANG['IT']['credits_label'], fg="#E0E0E0", bg="#121212", font=("Segoe UI", 10, "bold"))
credits_label.pack(pady=(10, 0))
limits_label = tk.Label(root, text=LANG['IT']['limits_label'], fg="#888888", bg="#121212", font=("Segoe UI", 8, "italic"))
limits_label.pack()

money_entry = tk.Entry(root, justify='center', bg="#2c2c2c", fg="#00FF41", font=("Consolas", 16), borderwidth=0)
money_entry.insert(0, "999999")
money_entry.pack(pady=10, padx=50, fill='x')

btn_extract = tk.Button(root, text=LANG['IT']['extract_button'], command=extract_saves, bg="#1f1f1f", fg="white", font=("Segoe UI", 9, "bold"), pady=8, cursor="hand2")
btn_extract.pack(pady=5, padx=40, fill='x')

btn_patch = tk.Button(root, text=LANG['IT']['patch_button'], command=patch_saves, bg="#1f1f1f", fg="#00FF41", font=("Segoe UI", 11, "bold"), pady=12, cursor="hand2")
btn_patch.pack(pady=5, padx=40, fill='x')

btn_restore = tk.Button(root, text=LANG['IT']['restore_button'], command=restore_saves, bg="#1f1f1f", fg="#FF6B6B", font=("Segoe UI", 9, "bold"), pady=8, cursor="hand2")
btn_restore.pack(pady=5, padx=40, fill='x')

# FOOTER E FIRMA
footer_label = tk.Label(root, text=LANG['IT']['footer'], fg="#666666", bg="#121212", font=("Arial", 7, "italic"))
footer_label.pack(side="bottom", pady=(0, 5))

signature_label = tk.Label(root, text=LANG['IT']['signature'], fg="#00FF41", bg="#121212", font=("Segoe UI", 9, "bold"))
signature_label.pack(side="bottom", pady=5)

root.mainloop()