import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from PIL import Image, ImageTk
import struct
import os
import sys
import shutil
import ctypes
import string

# --- ELEVAZIONE PRIVILEGI ADMIN ---
def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

# --- DIZIONARIO TRADUZIONI ---
LANG = {
    'IT': {
        'title': 'NFSU2 Profiles Master - GabriLex',
        'credits_label': 'CREDITI DA AGGIUNGERE',
        'limits': '(Min: 50 - Max: 999,999,999)',
        'list_label': 'PROFILI TROVATI NEL SISTEMA:',
        'path_label': 'Sorgente:',
        'btn_patch': 'PATCHA SOLDI',
        'btn_rename': 'RINOMINA PROFILO (SAFE)',
        'btn_backup': 'BACKUP SU DESKTOP',
        'btn_manual': 'CARICA MANUALE (FILE)',
        'footer': 'Need for Speed Underground 2 - Profile Editor',
        'signature': 'GabriLex vers. 1.0.1',
        'success': 'Operazione completata!',
        'error': 'Errore',
        'no_sel': 'Seleziona un profilo dalla lista!',
        'rename_prompt': 'Nuovo nome (max 7 caratteri):',
        'invalid_val': 'Inserisci un numero tra 50 e 999,999,999!',
        'backup_ok': 'Backup salvato in Desktop/NFSU2_BACKUPS'
    },
    'EN': {
        'title': 'NFSU2 Profiles Master - GabriLex',
        'credits_label': 'CREDITS TO ADD',
        'limits': '(Min: 50 - Max: 999,999,999)',
        'list_label': 'PROFILES FOUND IN SYSTEM:',
        'path_label': 'Source:',
        'btn_patch': 'PATCH MONEY',
        'btn_rename': 'RENAME PROFILE (SAFE)',
        'btn_backup': 'BACKUP TO DESKTOP',
        'btn_manual': 'MANUAL LOAD (FILE)',
        'footer': 'Need for Speed Underground 2 - Profile Editor',
        'signature': 'GabriLex vers. 1.0.1',
        'success': 'Operation successful!',
        'error': 'Error',
        'no_sel': 'Please select a profile from the list!',
        'rename_prompt': 'New name (max 7 chars):',
        'invalid_val': 'Enter a number between 50 and 999,999,999!',
        'backup_ok': 'Backup saved in Desktop/NFSU2_BACKUPS'
    }
}

class NFSU2Manager:
    def __init__(self, root):
        self.root = root
        self.current_lang = 'IT'
        self.all_saves = {}
        self.setup_ui()
        self.full_system_scan()

    def res_path(self, rel):
        """Gestisce i percorsi per PyInstaller e sviluppo"""
        try: base = sys._MEIPASS
        except: base = os.path.abspath(".")
        return os.path.join(base, rel)

    def setup_ui(self):
        self.root.title(LANG[self.current_lang]['title'])
        self.root.geometry("500x850")
        self.root.configure(bg="#0f0f0f")

        # --- ICONA FINESTRA ---
        try:
            self.root.iconbitmap(self.res_path("nfsu2_icon.ico"))
        except: pass

        # Menu Lingua
        top_bar = tk.Frame(self.root, bg="#0f0f0f")
        top_bar.pack(fill='x', padx=10, pady=5)
        self.lang_cb = ttk.Combobox(top_bar, values=['IT', 'EN'], width=5, state="readonly")
        self.lang_cb.set('IT')
        self.lang_cb.bind("<<ComboboxSelected>>", self.change_language)
        self.lang_cb.pack(side='right')

        # Header Image
        try:
            img = ImageTk.PhotoImage(Image.open(self.res_path("nfs.jpg")).resize((450, 200)))
            self.header = tk.Label(self.root, image=img, bg="#0f0f0f")
            self.header.image = img
            self.header.pack(pady=5)
        except: pass

        # Sezione Lista
        self.lbl_list = tk.Label(self.root, text=LANG[self.current_lang]['list_label'], fg="#00FF41", bg="#0f0f0f", font=("Segoe UI", 10, "bold"))
        self.lbl_list.pack()
        
        list_frame = tk.Frame(self.root, bg="#0f0f0f")
        list_frame.pack(pady=5, padx=40, fill='both', expand=True)
        self.scrollbar = tk.Scrollbar(list_frame)
        self.scrollbar.pack(side='right', fill='y')
        self.listbox = tk.Listbox(list_frame, bg="#1a1a1a", fg="#00FF41", font=("Consolas", 11), borderwidth=0, highlightthickness=1, yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side='left', fill='both', expand=True)
        self.scrollbar.config(command=self.listbox.yview)

        # Label Percorso
        self.lbl_path = tk.Label(self.root, text="", fg="#666666", bg="#0f0f0f", font=("Arial", 7), wraplength=400)
        self.lbl_path.pack()

        # Input Soldi con Limiti
        self.lbl_credits = tk.Label(self.root, text=LANG[self.current_lang]['credits_label'], fg="white", bg="#0f0f0f")
        self.lbl_credits.pack(pady=(10,0))
        self.lbl_limits = tk.Label(self.root, text=LANG[self.current_lang]['limits'], fg="#555", bg="#0f0f0f", font=("Arial", 8))
        self.lbl_limits.pack()
        
        self.money_entry = tk.Entry(self.root, justify='center', bg="#222", fg="#00FF41", font=("Consolas", 20), borderwidth=0)
        self.money_entry.insert(0, "999999")
        self.money_entry.pack(pady=5, padx=100, fill='x')

        # Pulsanti Tradotti
        self.btn_patch = self.add_btn(LANG[self.current_lang]['btn_patch'], self.patch_money, "#00FF41", "black")
        self.btn_rename = self.add_btn(LANG[self.current_lang]['btn_rename'], self.safe_rename, "white", "black")
        self.btn_backup = self.add_btn(LANG[self.current_lang]['btn_backup'], self.backup_save, "#3498db", "white")
        self.btn_manual = self.add_btn(LANG[self.current_lang]['btn_manual'], self.manual_load, "#f1c40f", "black")

        # Footer
        self.lbl_sig = tk.Label(self.root, text="GabriLex vers. 1.0.1", fg="#00FF41", bg="#0f0f0f", font=("Segoe UI", 10, "bold"))
        self.lbl_sig.pack(side="bottom", pady=5)
        self.lbl_foot = tk.Label(self.root, text=LANG[self.current_lang]['footer'], fg="#444", bg="#0f0f0f", font=("Arial", 7, "italic"))
        self.lbl_foot.pack(side="bottom")

    def add_btn(self, txt, cmd, bg, fg):
        btn = tk.Button(self.root, text=txt, command=cmd, bg=bg, fg=fg, font=("Segoe UI", 10, "bold"), pady=10, cursor="hand2", relief='flat')
        btn.pack(pady=4, padx=50, fill='x')
        return btn

    def change_language(self, e=None):
        self.current_lang = self.lang_cb.get()
        # Aggiornamento UI
        self.root.title(LANG[self.current_lang]['title'])
        self.lbl_list.config(text=LANG[self.current_lang]['list_label'])
        self.lbl_credits.config(text=LANG[self.current_lang]['credits_label'])
        self.lbl_limits.config(text=LANG[self.current_lang]['limits'])
        self.btn_patch.config(text=LANG[self.current_lang]['btn_patch'])
        self.btn_rename.config(text=LANG[self.current_lang]['btn_rename'])
        self.btn_backup.config(text=LANG[self.current_lang]['btn_backup'])
        self.btn_manual.config(text=LANG[self.current_lang]['btn_manual'])
        self.lbl_foot.config(text=LANG[self.current_lang]['footer'])
        self.full_system_scan()

    def full_system_scan(self):
        self.listbox.delete(0, tk.END)
        self.all_saves = {}
        search_dirs = [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'NFS Underground 2'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'VirtualStore', 'Program Files (x86)', 'EA GAMES', 'NFS Underground 2')
        ]
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                search_dirs.append(os.path.join(drive, 'Games', 'NFS Underground 2'))
        
        for base in search_dirs:
            if os.path.exists(base):
                for root_dir, _, files in os.walk(base):
                    f_name = os.path.basename(root_dir)
                    if f_name in files:
                        self.all_saves[f_name] = os.path.join(root_dir, f_name)
                        self.listbox.insert(tk.END, f_name)
        
        self.lbl_path.config(text=f"{LANG[self.current_lang]['path_label']} {len(self.all_saves)} profiles")

    def patch_money(self):
        idx = self.listbox.curselection()
        if not idx: return messagebox.showwarning("!", LANG[self.current_lang]['no_sel'])
        path = self.all_saves[self.listbox.get(idx)]
        try:
            val = int(self.money_entry.get())
            if 50 <= val <= 999999999:
                with open(path, "rb+") as f:
                    f.seek(41322)
                    f.write(struct.pack("<I", val))
                messagebox.showinfo("OK", LANG[self.current_lang]['success'])
            else:
                messagebox.showerror("Range", LANG[self.current_lang]['invalid_val'])
        except: messagebox.showerror("Err", LANG[self.current_lang]['error'])

    def safe_rename(self):
        idx = self.listbox.curselection()
        if not idx: return
        old_n = self.listbox.get(idx).split(" [")[0] # Gestisce nomi caricati manualmente
        path = self.all_saves[self.listbox.get(idx)]
        new_n = simpledialog.askstring("Rename", LANG[self.current_lang]['rename_prompt'])
        if not new_n: return
        new_n = new_n[:7].strip()
        try:
            with open(path, "rb") as f: data = bytearray(f.read())
            data = data.replace(old_n.encode(), new_n.encode().ljust(len(old_n), b'\x00'))
            with open(path, "wb") as f: f.write(data)
            
            old_dir = os.path.dirname(path)
            os.rename(path, os.path.join(old_dir, new_n))
            os.rename(old_dir, os.path.join(os.path.dirname(old_dir), new_n))
            self.full_system_scan()
            messagebox.showinfo("OK", LANG[self.current_lang]['success'])
        except Exception as e: messagebox.showerror("Err", str(e))

    def backup_save(self):
        idx = self.listbox.curselection()
        if not idx: return
        path = self.all_saves[self.listbox.get(idx)]
        dest = os.path.join(os.path.expanduser("~"), "Desktop", "NFSU2_BACKUPS")
        os.makedirs(dest, exist_ok=True)
        shutil.copy2(path, os.path.join(dest, os.path.basename(path) + ".bak"))
        messagebox.showinfo("OK", LANG[self.current_lang]['backup_ok'])

    def manual_load(self):
        f = filedialog.askopenfilename()
        if f:
            n = f"{os.path.basename(f)} [MANUAL]"
            self.all_saves[n] = f
            self.listbox.insert(tk.END, n)

if __name__ == "__main__":
    root = tk.Tk()
    app = NFSU2Manager(root)
    root.mainloop()