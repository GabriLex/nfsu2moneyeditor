import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from PIL import Image, ImageTk
import struct
import os
import sys
import shutil
import ctypes

# --- ELEVAZIONE PRIVILEGI ADMIN ---
def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

# --- DATI MAZDA MX-5 ---
MAZDA_DATA = [
    {"off": 0x5870, "hex": "40 C9 33 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 6B 5D 45 03 A5 E0 9B C6 04 C2 2F 32 45 15 FC 6B 00 00 00 00 00 00 00 00 DF C3 1E 7C 96 0A 62 92 85 E2 70 0B BD A2 71 B8 7B 0F 22 7C 25 E5 3E 01 7E C3 28 01 EF F0 78 FA 67 04 CE 05 9B D6 F4 12 EE E9 5C 4E F3 FC EF D6 AF 5C 46 D3 22 BA 80 3C 7E 7F 72 12 D1 36 31 61 A2 27 5B A4 75 E3 2E 30 00 00 00 00 00 00 00 00 58 A6 34 17 82 93 09 54 9E 7A 83 01 9E 7A 83 01 AE 11 FA 02 AE 11 FA 02 00 00 00 00 00 DC 45 F3 68 8E A3 53 96 80 A3 52 05 47 C9 FA 05 47 C9 FA AD 09 64 45 AD 09 64 45 97 4E 44 FA 97 4E 44 FA 05 47 C9 FA 05 47 C9 FA 05 47 C9 FA 05 47 C9 FA AD 09 64 45 AD 09 64 45 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 39 C8 49 8B 2A 7D 2D E2 CB BB 0F AE 6D 14 19 34 00 66 ED 12 7D C5 41 56 30 12 51 E1 C6 F1 F3 55 79 EE 23 70 36 50 3C DB 09 F4 9C 05 8A 9A CD ED 00 00 00 00 00 00 00 00"},
    {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 A3 86 60 2C"},
    {"off": 0xAD80, "hex": "8C 9A 31 01 4D 32 35 C4 6A E0 5B C4 1E 38 92 41 00 00 00 00 20 51 70 39 D5 44 01 00 00 00 00 00"},
    {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 C2 C5 00 00 17 D6 04 00 B8 D0 81 00 37 F2 79 00 5B 1D 08 00 B2 6A E0 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
]

LANG = {
    'IT': {
        'list': 'PROFILI TROVATI NEL SISTEMA:', 'mazda': 'MOD: MAZDA MX-5 SWAP',
        'patch': 'PATCHA SOLDI', 'rename': 'RINOMINA PROFILO (SAFE)', 'backup': 'BACKUP SU DESKTOP',
        'manual': 'CARICA MANUALE (FILE)', 'prompt': 'Nuovo nome (Max 7 car.):', 'success': 'Fatto!'
    },
    'EN': {
        'list': 'PROFILES FOUND IN SYSTEM:', 'mazda': 'MOD: MAZDA MX-5 SWAP',
        'patch': 'PATCH MONEY', 'rename': 'RENAME PROFILE (SAFE)', 'backup': 'BACKUP TO DESKTOP',
        'manual': 'MANUAL LOAD (FILE)', 'prompt': 'New name (Max 7 chars):', 'success': 'Success!'
    }
}

class NFSU2App:
    def __init__(self, root):
        self.root = root
        self.version = "1.0.2"
        self.lang = 'IT'
        self.all_saves = {}
        self.setup_ui()
        self.full_scan()

    def get_res(self, p):
        try: b = sys._MEIPASS
        except: b = os.path.abspath(".")
        return os.path.join(b, p)

    def setup_ui(self):
        self.root.title("NFSU2 Profiles Master - GabriLex")
        self.root.geometry("450x880")
        self.root.configure(bg="#0f0f0f")
        try: self.root.iconbitmap(self.get_res("icona.ico"))
        except: pass

        self.lang_cb = ttk.Combobox(self.root, values=["IT", "EN"], width=5, state="readonly")
        self.lang_cb.set("IT")
        self.lang_cb.pack(anchor="ne", padx=10, pady=5)
        self.lang_cb.bind("<<ComboboxSelected>>", self.update_lang)

        try:
            img = Image.open(self.get_res("header.png")).resize((410, 210))
            self.header_img = ImageTk.PhotoImage(img)
            tk.Label(self.root, image=self.header_img, bg="#0f0f0f").pack()
        except: tk.Frame(self.root, width=410, height=210, bg="#222").pack()

        self.lbl_list = tk.Label(self.root, text=LANG[self.lang]['list'], fg="#00FF41", bg="#0f0f0f", font=("Segoe UI", 10, "bold"))
        self.lbl_list.pack(pady=5)
        
        self.listbox = tk.Listbox(self.root, bg="#1a1a1a", fg="#00FF41", font=("Consolas", 11), height=8, borderwidth=1, relief="solid")
        self.listbox.pack(pady=5, padx=25, fill="x")

        self.btn_mazda = self.add_btn(LANG[self.lang]['mazda'], self.apply_mazda, "#C0392B", "white")
        self.money_entry = tk.Entry(self.root, justify="center", bg="#1a1a1a", fg="#00FF41", font=("Consolas", 24), borderwidth=0)
        self.money_entry.insert(0, "999999")
        self.money_entry.pack(pady=15, padx=80, fill="x")
        self.btn_patch = self.add_btn(LANG[self.lang]['patch'], self.apply_money, "#00FF41", "black")
        self.btn_rename = self.add_btn(LANG[self.lang]['rename'], self.apply_rename, "white", "black")
        self.btn_backup = self.add_btn(LANG[self.lang]['backup'], self.apply_backup, "#2980B9", "white")
        self.btn_manual = self.add_btn(LANG[self.lang]['manual'], self.manual_load, "#F1C40F", "black")
        
        tk.Label(self.root, text=f"GabriLex vers. {self.version}", fg="#00FF41", bg="#0f0f0f", font=("Segoe UI", 10, "bold")).pack(side="bottom", pady=10)

    def add_btn(self, t, c, b, f):
        btn = tk.Button(self.root, text=t, command=c, bg=b, fg=f, font=("Segoe UI", 11, "bold"), relief="flat", pady=8, cursor="hand2")
        btn.pack(pady=5, padx=45, fill="x")
        return btn

    def update_lang(self, e):
        self.lang = self.lang_cb.get()
        self.lbl_list.config(text=LANG[self.lang]['list'])
        self.btn_mazda.config(text=LANG[self.lang]['mazda'])
        self.btn_patch.config(text=LANG[self.lang]['patch'])
        self.btn_rename.config(text=LANG[self.lang]['rename'])
        self.btn_backup.config(text=LANG[self.lang]['backup'])
        self.btn_manual.config(text=LANG[self.lang]['manual'])

    def full_scan(self):
        self.listbox.delete(0, tk.END)
        paths = [os.path.join(os.environ.get('LOCALAPPDATA', ''), 'NFS Underground 2'), 
                 os.path.join(os.environ.get('PROGRAMDATA', ''), 'NFS Underground 2'),
                 os.path.join(os.path.expanduser('~'), 'Documents', 'NFS Underground 2')]
        for b in paths:
            if os.path.exists(b):
                for d in os.listdir(b):
                    p = os.path.join(b, d, d)
                    if os.path.exists(p):
                        self.all_saves[d] = p
                        self.listbox.insert(tk.END, d)

    def apply_mazda(self):
        idx = self.listbox.curselection()
        if not idx: return
        path = self.all_saves[self.listbox.get(idx)]
        with open(path, "rb+") as f:
            for b in MAZDA_DATA:
                f.seek(b["off"])
                f.write(bytes.fromhex(b["hex"].replace(" ", "")))
        messagebox.showinfo("OK", LANG[self.lang]['success'])

    def apply_money(self):
        idx = self.listbox.curselection()
        if not idx: return
        path = self.all_saves[self.listbox.get(idx)]
        with open(path, "rb+") as f:
            f.seek(41322)
            f.write(struct.pack("<I", int(self.money_entry.get())))
        messagebox.showinfo("OK", LANG[self.lang]['success'])

    def apply_rename(self):
        idx = self.listbox.curselection()
        if not idx: return
        old_n = self.listbox.get(idx)
        new_n = simpledialog.askstring("Rename", LANG[self.lang]['prompt'])
        if not new_n: return
        
        # Logica 7 caratteri + padding 00
        new_n = new_n.strip()[:7]
        new_bytes = new_n.encode().ljust(7, b'\x00')
        
        old_path = self.all_saves[old_n]
        old_dir = os.path.dirname(old_path)
        
        try:
            with open(old_path, "rb+") as f:
                # SCRIVE SOLO ALL'OFFSET D220 + 5 (COLONNA 05)
                f.seek(0xD220 + 5)
                f.write(new_bytes)
            
            # Rinomina fisica dei file per la compatibilità OS
            new_file_path = os.path.join(old_dir, new_n)
            os.rename(old_path, new_file_path)
            new_dir = os.path.join(os.path.dirname(old_dir), new_n)
            os.rename(old_dir, new_dir)
            
            self.full_scan()
            messagebox.showinfo("OK", LANG[self.lang]['success'])
        except Exception as e: messagebox.showerror("Err", str(e))

    def apply_backup(self):
        idx = self.listbox.curselection()
        if not idx: return
        src = self.all_saves[self.listbox.get(idx)]
        dst = os.path.join(os.path.expanduser("~"), "Desktop", "NFSU2_Backups")
        os.makedirs(dst, exist_ok=True)
        shutil.copy2(src, os.path.join(dst, os.path.basename(src)))
        messagebox.showinfo("OK", "Backup creato!")

    def manual_load(self):
        f = filedialog.askopenfilename()
        if f:
            name = os.path.basename(f)
            self.all_saves[name] = f
            self.listbox.insert(tk.END, name)

if __name__ == "__main__":
    root = tk.Tk()
    app = NFSU2App(root)
    root.mainloop()