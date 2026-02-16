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

# --- DIZIONARIO LINGUE ---
LANG = {
    'IT': {
        'title': 'NFSU2 Profiles Master - GabriLex',
        'profiles': 'PROFILI TROVATI:',
        'select_car': 'SELEZIONA AUTO:',
        'inject_btn': 'INNIETTA AUTO',
        'money': 'SOLDI:',
        'patch_btn': 'PATCHA SOLDI',
        'rename_btn': 'RINOMINA PROFILO (SAFE)',
        'backup_btn': 'BACKUP SU DESKTOP',
        'footer': 'Need for Speed Underground 2 Editor - Versione 1.0.3',
        'success_inject': 'Auto iniettata con successo!',
        'success_money': 'Soldi aggiornati!',
        'success_rename': 'Rinomina completata!',
        'rename_prompt': 'Nuovo nome (Max 7 car.):',
        'err_select': 'Seleziona un profilo!',
        'err_admin': 'Errore: Chiudi il gioco prima di procedere!'
    },
    'EN': {
        'title': 'NFSU2 Profiles Master - GabriLex',
        'profiles': 'PROFILES FOUND:',
        'select_car': 'SELECT CAR:',
        'inject_btn': 'INJECT CAR',
        'money': 'MONEY:',
        'patch_btn': 'PATCH MONEY',
        'rename_btn': 'RENAME PROFILE (SAFE)',
        'backup_btn': 'BACKUP TO DESKTOP',
        'footer': 'Need for Speed Underground 2 Editor - Version 1.0.3',
        'success_inject': 'Car injected successfully!',
        'success_money': 'Money updated!',
        'success_rename': 'Rename completed!',
        'rename_prompt': 'New name (Max 7 chars):',
        'err_select': 'Select a profile first!',
        'err_admin': 'Error: Close the game before proceeding!'
    }
}

# --- DATABASE AUTO (POPOLALO CON I TUOI DATI TESTATI) ---
CAR_DATABASE = {
    "Mitsubishi Lancer Evo VIII": [
        {"off": 0x5870, "hex": "5C 1B 9A 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 F6 EF D2 09 10 C2 B1 C2 AF 42 56 35 90 AC AF D8 00 00 00 00 00 00 00 00 8A C9 F0 8F A1 C5 74 20 85 E2 70 0B C8 82 4B 99 26 15 F4 8F 30 A0 51 8F 89 7E 3B 8F BA 9A 26 58 D2 20 38 56 26 1F B4 92 D9 43 05 C6 BE A6 9D 34 3A A5 05 53 0D 14 29 B4 49 C4 66 52 FC 14 AE 9F 0D 7F 24 0B 40 28 23 70 00 00 00 00 00 00 00 00 43 00 DD 8E CD 2A BD C0 E9 11 37 6E E9 11 37 6E F9 A8 AD 6F F9 A8 AD 6F"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 64 A6 C6 C9 55 56 8F 57 96 9B B5 0E 78 85 9E 1D 6B F8 20 2D A8 9E A3 CB BB 10 EE 02 11 BF CA 52 24 65 D4 07 A1 1D E5 20 D4 6E 5F 00 E5 BD BC B8 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 4E 11 29 14"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 54 32 35 C4 62 E0 5B C4 C5 F1 91 41 00 00 00 00 20 51 F5 D5 04 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 00 00 00 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 1F B5 00 00 1C 3D 04 00 88 27 6F 00 67 1B 6F 00 4C 0C 15 00 12 10 A4 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Mitsubishi 3000GT": [
        {"off": 0x5870, "hex": "F2 3B 96 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 5D 9B 7C 2D D7 A5 61 6A B6 B6 1D 66 B7 3B C5 46 00 00 00 00 00 00 00 00 91 26 44 B9 88 C3 33 74 85 E2 70 0B AF 89 1A 87 2D 72 47 B9 17 9E 10 E3 70 7C FA E2 61 AE 9C 97 99 DB D6 21 8D B8 FD 87 20 0A 82 64 65 BA 13 74 A1 3E 4F 48 54 DA A5 52 F0 8E 6D E1 83 34 8E 0F D4 10 99 8B E7 F2 29 FF 00 00 00 00 00 00 00 00 8A C6 59 2D F4 B9 D2 2E 10 A1 4C DC 10 A1 4C DC 20 38 C3 DD 20 38 C3 DD 00 00 00 00 72 02 0F CE 68 8E A3 53 08 A7 6C 2D 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 EB C5 A6 39 DC 0C BE 26 3D 1D 14 72 5F 71 52 04 32 61 52 EA 2F 55 D2 9A 22 98 F3 B7 38 BC 4F 5F 2B 07 F9 A4 68 5D BA 99 7B A7 DC 93 E7 BD BC B8 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 55 57 2F 61"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 A7 32 35 C4 05 E0 5B C4 05 DB 91 41 00 00 00 00 20 51 72 FC D3 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 B7 D4 6F 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 BF BA 00 00 F1 DD 41 00 38 24 78 00 4F 47 70 00 9F 16 38 00 AE F2 A9 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Mitsubishi Eclipse GSX ": [
        {"off": 0x5870, "hex": "3C C1 5F 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 84 DA 02 75 5E 75 A0 A5 7D A6 45 52 9E CE 3A 84 00 00 00 00 00 00 00 00 58 3F 18 DA 2F F5 8A AF 85 E2 70 0B 56 04 6A 98 F4 8A 1B DA BE CF 67 1E 17 AE 51 1E C8 E5 86 05 20 42 14 C8 B4 65 53 19 27 5C 8D 20 CC F1 FD E1 C8 EB A4 D9 5B 2C B1 0E 57 3D B0 33 CA AF 26 AA 5B 0E 7C 21 4E A1 6C 51 00 00 00 00 00 00 00 00 91 18 65 E9 DB 4C 48 6C F7 33 C2 19 F7 33 C2 19 07 CB 38 1B 07 CB 38 1B 00 00 00 00 59 95 84 0B 68 8E A3 53 EF 39 E2 6A 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 32 41 3F D4 23 DF 24 F2 A4 42 36 59 06 11 0E 8E B9 F5 81 AB 76 27 39 66 49 B3 34 F0 1F 3D 44 AC F2 A4 7D 90 EF 88 DD 78 E2 43 65 57 E4 BD BC B8 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 1C 99 96 E5"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 99 32 35 C4 05 E0 5B C4 52 4A 92 41 00 00 00 00 20 51 94 AB D4 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 B7 99 72 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 C2 C2 00 00 70 4E 04 00 78 7C 7D 00 C7 9E 75 00 3A 72 08 00 6A 9C B9 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Infiniti G35 Coupe": [
        {"off": 0x5870, "hex": "6B EB 8D 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 6E A8 00 00 88 85 1D EA 27 B8 16 6E 08 53 FB 27 00 00 00 00 00 00 00 00 02 47 2F 0D 19 F2 82 45 85 E2 70 0B 40 B7 10 E8 9E 92 32 0D A8 CC 5F B4 01 AB 49 B4 32 C5 71 F9 4A DC 0B 1D 9E C7 73 B3 51 FB B9 FE 36 D1 E8 D5 B2 4D C5 73 85 CB DD EC C1 E6 90 13 74 86 1C 86 85 32 D8 75 B8 4A 4D 31 00 00 00 00 00 00 00 00 BB B7 91 C7 45 D1 08 10 61 B8 82 BD 61 B8 82 BD 71 4F F9 BE 71 4F F9 BE 00 00 00 00 C3 19 45 AF 68 8E A3 53 59 BE A2 0E 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 DC 17 35 B0 CD BF 33 54 0E B6 36 7B F0 A1 A6 E7 E3 A3 2C 38 20 08 48 C8 33 A9 1F 94 89 55 C4 F6 9C CA 00 2B 19 C1 C0 C0 4C 81 AF 9B 4F F9 6E 3C 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 C6 96 5D 5C"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 43 32 35 C4 61 E0 5B C4 60 A0 91 41 00 00 00 00 20 51 79 38 D4 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 B7 D4 6F 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 65 60 02 00 97 83 43 00 30 F9 79 00 47 1C 72 00 55 1C 3C 00 64 F8 AD 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Nissan 240SX": [
        {"off": 0x5870, "hex": "41 EC 43 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 80 FB 50 01 DA 93 96 03 F9 6D 31 5C 9A 96 CD 9B 00 00 00 00 00 00 00 00 D4 4A E2 F4 2B 70 96 23 85 E2 70 0B 52 43 98 F0 70 96 E5 F4 BA 4A 73 92 13 29 5D 92 C4 0F 5D AA 9C 1C 8F BD B0 FE 5B 4C A3 14 A9 B4 C8 1B D4 86 C4 84 AD 0C D7 E4 CC A2 53 A3 1E E7 46 D5 61 CB D7 A4 77 55 4A 07 DB 04 00 00 00 00 00 00 00 00 0D D1 80 7D D7 14 DB 83 F3 FB 54 31 F3 FB 54 31 03 93 CB 32 03 93 CB 32 00 00 00 00 55 5D 17 23 68 8E A3 53 EB 01 75 82 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 AE 66 7A F5 9F C0 FB 86 A0 E4 B8 5D 02 04 48 1C 35 48 FA 00 F2 08 10 FB 45 C4 E7 1F 1B 7D FF 94 6E E4 A0 90 6B 97 CE 0E DE 21 78 AB 97 43 EE 98 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 98 E8 3A C9"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 D8 CD 35 C4 67 E0 5B C4 EC E3 91 41 00 00 00 00 20 51 B1 40 D5 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 B7 D4 6F 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 8C D0 00 00 E1 E0 04 00 68 09 82 00 E7 2A 7A 00 7F 97 0A 00 D6 E4 E2 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Nissan 350Z": [
        {"off": 0x5870, "hex": "AA 52 9E 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 D1 C6 0A 00 CB 19 19 62 AA 05 77 C8 2B 7C F6 22 00 00 00 00 00 00 00 00 85 C1 07 26 FC BC 6A 79 85 E2 70 0B 23 4F F9 02 21 0D 0B 26 8B 97 47 E8 E4 75 31 E8 D5 D4 77 C6 8D 03 ED CD 01 4C 3C DA 14 0C 93 FE D9 E0 EE A2 15 D2 8D 9A 48 DC B6 EC 64 E9 71 FC 77 DD 1D 8B C8 EC 81 E9 5B 4D 2E 1A 00 00 00 00 00 00 00 00 7E C8 6A C7 68 FA 03 0B 84 E1 7D B8 84 E1 7D B8 94 78 F4 B9 94 78 F4 B9 00 00 00 00 E6 42 40 AA 68 8E A3 53 7C E7 9D 09 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 DF 6E 36 B5 D0 69 11 72 B1 AB 35 D9 D3 D2 15 2D 26 F1 81 2B 23 B2 25 E6 96 93 B2 6D AC 64 BB 80 1F BE D9 F3 5C A1 A4 23 EF 69 0F 5B 93 43 EE 98 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 49 3E D1 E8"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 9B 5C 35 C4 39 21 5B C4 0D F0 91 41 00 00 00 00 20 51 B7 44 D4 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 B7 D4 6F 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 CA E0 00 00 FC 03 04 00 D8 58 7A 00 EF 7B 72 00 B0 1D 3F 00 BF F9 B0 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Nissan Skyline R34": [
        {"off": 0x5870, "hex": "27 EA 88 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 5E 37 48 BE 78 EA 23 19 17 01 73 69 F8 3D 7A B3 00 00 00 00 00 00 00 00 F2 9F 09 D3 09 69 A8 C6 85 E2 70 0B 30 3E 66 8C 8E EB 0C D3 98 43 85 35 F1 21 6F 35 22 B8 D0 59 3A 31 E0 C2 8E 36 5B A7 41 48 8F 6F 26 C4 47 36 A2 BC AC 67 75 18 B3 5D B1 C9 6B C9 64 C7 53 F7 75 77 6A B9 A8 2D 28 E7 00 00 00 00 00 00 00 00 AB 04 67 38 35 BC 87 9B 51 A3 01 49 51 A3 01 49 61 3A 78 4A 61 3A 78 4A 00 00 00 00 B3 04 C4 3A 68 8E A3 53 49 A9 21 9A 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 CC 58 6C 21 BD F0 54 5D FE 88 7D 7B E0 F8 3B 2D D3 D8 6C 30 10 39 69 D1 23 F8 66 C1 79 20 1B 93 8C F3 30 52 09 E6 9E 74 3C 44 52 CB E4 BD BC B8 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 B6 FF A5 97"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 22 32 35 C4 6F E0 5B C4 7A 82 92 41 00 00 00 00 20 51 78 E1 04 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 00 00 00 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 47 DD 00 00 44 65 04 00 78 81 6F 00 57 75 6F 00 8C 7D 17 00 52 81 A6 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Nissan Sentra SE-R Spec V": [
        {"off": 0x5870, "hex": "6A A9 4D 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 EC BF AE 79 C6 FB 1B 6D E5 42 78 CD 06 7E D7 0B 00 00 00 00 00 00 00 00 C0 F3 48 53 97 36 D2 4E 85 E2 70 0B BE 5D DA 31 5C 3F 4C 53 26 11 AF BD 7F EF 98 BD 30 21 A4 93 88 B0 43 50 1C 1B AD A3 8F BE 1D F6 34 2D 1B 70 30 A1 FE 63 C3 8E 41 E4 BF 60 66 8F 32 40 A1 7C C3 64 C7 33 B6 C4 22 AD 00 00 00 00 00 00 00 00 F9 7A F5 BE 43 FC E4 F3 5F E3 5E A1 5F E3 5E A1 6F 7A D5 A2 6F 7A D5 A2 00 00 00 00 C1 44 21 93 68 8E A3 53 57 E9 7E F2 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 9A D1 B9 A6 8B 57 BD F0 0C 4E ED 60 6E 22 3B D6 21 34 51 F9 DE 9F D1 64 B1 38 DC C1 87 BC E2 85 5A 11 EC 9D 57 AF 98 9B 4A 37 85 D1 E5 BD BC B8 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 FA 26 AF 42"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 88 32 35 C4 66 E0 5B C4 6B 52 92 41 00 00 00 00 20 51 D8 FB D4 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 B7 99 72 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 09 D2 00 00 B7 5D 04 00 88 EF 7F 00 D7 11 78 00 C7 19 21 00 F7 43 D2 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Subaru Impreza": [
        {"off": 0x5870, "hex": "08 D5 A6 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 F8 58 44 CF 52 1C 17 89 71 68 7B FD 12 22 06 F6 00 00 00 00 00 00 00 00 4C 4D F5 9F A3 C1 09 31 85 E2 70 0B CA 9C 6D 1B E8 98 F8 9F 32 9C E6 9F 8B 7A D0 9F 3C 9F EA E1 14 9D 6C 79 28 4C 8B 9D 1B 11 C2 2B 40 AB 61 BE 3C D2 DC 5D 4F E1 E5 19 CB 2A 20 79 BE 4B 94 9D 4F 1D 2A 71 C2 8E DC 96 00 00 00 00 00 00 00 00 85 CD 99 F4 4F A0 13 DE 6B 87 8D 8B 6B 87 8D 8B 7B 1E 04 8D 7B 1E 04 8D 00 00 00 00 CD E8 4F 7D 68 8E A3 53 63 8D AD DC 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 2A 6B A8 83 1B 81 34 C1 9C 85 5D E3 FE 35 18 2D B1 B9 D0 2B 6E C9 48 35 41 94 38 A1 17 3C C4 AD EA 82 FD C1 E7 C4 CC 09 DA FE 3B 06 EB BD BC B8 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 10 F3 8E E9"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 4E CD 35 C4 05 E0 5B C4 B4 73 92 41 00 00 00 00 20 51 2B C0 04 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 00 00 00 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 FF 9A 00 00 FC 22 04 00 50 7D 20 00 2F 71 20 00 82 B7 10 00 48 BB 9F 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Toyota Celica": [
        {"off": 0x5870, "hex": "CD 0F 72 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 60 EC 5A 54 BA 10 DA 84 D9 F2 5D CE 7A FF 0C C6 00 00 00 00 00 00 00 00 B4 EF C7 AC 0B B1 30 D8 85 E2 70 0B 32 A4 EF A6 50 3B CB AC 9A 8B 0D 47 F3 69 F7 46 A4 08 8B EE 7C 79 71 05 90 AF EB 53 83 E1 2E AE A8 14 02 CB A4 35 3D 14 B7 B1 52 9C 33 7C A7 82 26 CA 05 D8 B7 E1 D8 04 2A E0 63 A0 00 00 00 00 00 00 00 00 ED 9D 06 77 B7 7D 1A AE D3 64 94 5B D3 64 94 5B E3 FB 0A 5D E3 FB 0A 5D 00 00 00 00 35 C6 56 4D 68 8E A3 53 CB 6A B4 AC 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 8E 5B 1E 02 7F 95 36 0F 80 9D 7C ED E2 04 08 BC 15 65 BA 98 D2 DD 4A 83 25 35 7D AF FB A5 B4 5F 4E 29 FB B1 4B 94 CD EF BE BA 56 AC E5 BD BC B8 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 78 AD B9 AF"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 4E 36 35 C4 85 E0 5B C4 62 18 92 41 00 00 00 00 20 51 83 F4 D4 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 B7 99 72 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 C5 14 06 00 73 A0 04 00 40 B6 7F 00 8F D8 77 00 3C A8 1E 00 6C D2 CF 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Toyota Supra": [
        {"off": 0x5870, "hex": "D7 9B 66 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 8A C4 B8 03 24 93 97 92 C3 66 2A 84 24 9E C5 A4 00 00 00 00 00 00 00 00 9E 19 BC 46 35 18 AA B0 85 E2 70 0B 5C 81 71 04 3A 65 BF 46 C4 F2 86 1F 1D D1 70 1F 4E E2 FA CA E6 C5 17 ED BA 9B B8 0B ED 52 99 5F 52 EE 71 A7 CE 21 0A CC 21 23 BD 4D DD 5F 83 34 10 23 5E C5 21 F8 91 5F D4 C3 3F 52 00 00 00 00 00 00 00 00 57 0F 71 28 61 1C D3 8C 7D 03 4D 3A 7D 03 4D 3A 8D 9A C3 3B 8D 9A C3 3B 00 00 00 00 DF 64 0F 2C 68 8E A3 53 75 09 6D 8B 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 78 B4 76 EF 69 38 26 15 2A 8B 2E FD 0C 80 2E 28 7F 45 B0 89 BC 80 3A 89 4F 35 61 73 A5 58 99 AC 38 31 76 9B B5 3E 2A 24 68 B2 48 6C 3D DB AF 9E 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 62 8D 7F 74"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 94 32 35 C4 61 E0 5B C4 02 10 92 41 00 00 00 00 20 51 81 DD D4 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 B7 99 72 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 99 B2 00 00 47 3E 04 00 A6 02 7F 00 CF 24 77 00 49 6C 12 00 79 96 C3 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Toyota Trueno AE86 (Corolla)": [
        {"off": 0x5870, "hex": "14 1F 10 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 EB 13 7C F7 25 A7 08 82 84 E8 35 5D C5 6B 97 A3 00 00 00 00 00 00 00 00 5F 6A A6 20 16 81 DE C7 85 E2 70 0B 3D 99 1F BE FB B5 A9 20 A5 5B BB 36 FE 39 A5 36 6F 07 ED 80 E7 4A D9 EA 1B 8D C8 06 6E 70 A7 BC 73 13 64 5D 2F 13 1A C7 A2 40 CB AA FE 15 D5 BC 51 9D E6 57 22 EE 84 A9 F5 79 91 DA 00 00 00 00 00 00 00 00 D8 2C 7F 85 02 EA A4 8B 1E D1 1E 39 1E D1 1E 39 2E 68 95 3A 2E 68 95 3A 00 00 00 00 80 32 E1 2A 68 8E A3 53 16 D7 3E 8A 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 B9 2E FF 81 AA 63 21 91 4B D2 E0 C2 ED 8A B2 BC 80 AC B5 AE FD AB 35 05 B0 C8 C1 6E 46 48 6C 02 F9 14 A7 AB B6 16 23 04 89 8A 5C 4B A5 9A CD ED 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 23 AD E9 A0"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 25 33 35 C4 71 E0 5B C4 BE 3E 92 41 00 00 00 00 20 51 0E 4F D5 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 0F 5A 78 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 C0 ED 00 00 15 FE 04 00 A0 79 82 00 1F 9B 7A 00 F2 BA 0C 00 49 08 E5 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Ford Focus": [
        {"off": 0x5870, "hex": "D3 1B 2F 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 DF 04 CA 02 99 50 B7 B4 F8 0C 36 CC B9 D1 2A 80 00 00 00 00 00 00 00 00 D3 5A 53 31 0A 80 29 EE 85 E2 70 0B 31 E4 24 B0 6F A6 56 31 99 5A 06 5D F2 38 F0 5C 63 93 F3 65 5B 28 84 DA 0F E6 A1 47 E2 E7 AB 18 67 9F 6A 42 23 6C F3 07 16 B8 CF 06 F2 55 D2 DF C5 DB 8B DA 96 FF 1F D9 E9 B9 8E FD 00 00 00 00 00 00 00 00 4C A4 83 E1 F6 4F 38 68 12 37 B2 15 12 37 B2 15 22 CE 28 17 22 CE 28 17 00 00 00 00 74 98 74 07 68 8E A3 53 0A 3D D2 66 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 27 4F E0 D3 18 12 9B CF F9 6A 87 CC 1B 20 DF 08 6E E7 74 80 6B 5A AF 43 DE 44 71 7C F4 87 EB 39 67 4A 0E D3 A4 5F 2D A2 37 F1 AF AA 4F F9 6E 3C 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 91 AA A6 55"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 A7 32 35 C4 05 E0 5B C4 27 AD 91 41 00 00 00 00 20 51 AD ED 04 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 00 00 00 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 96 A2 06 00 88 6C 04 00 A6 67 20 00 75 67 20 00 A0 51 43 00 59 43 3D 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Ford Mustang GT": [
        {"off": 0x5870, "hex": "40 CB 8E 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 19 58 16 35 13 B8 FA 59 F2 01 EC 77 73 0F 19 6E 00 00 00 00 00 00 00 00 CD F5 88 DA 44 7A 12 BE 85 E2 70 0B 6B 44 7C 0A 69 41 8C DA D3 54 EF 2C 2C 33 D9 2C 1D 04 04 D4 D5 69 8C A7 49 6D 91 7B 5C 56 8C CA 21 10 7B B0 5D F3 E2 3B 90 26 B0 B8 AC E0 BC 71 BF BD C7 A9 10 1B 27 4A A3 44 79 8F 00 00 00 00 00 00 00 00 C6 12 64 93 B0 8D 26 56 CC 74 A0 03 CC 74 A0 03 DC 0B 17 05 DC 0B 17 05 00 00 00 00 2E D6 62 F5 68 8E A3 53 C4 7A C0 54 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 2D 6D A4 04 1E D6 87 D4 3F C6 48 39 E1 F1 E4 5C F4 F1 34 55 71 1E 9C 48 A4 89 F6 1E 3A 16 D5 92 6D A1 29 49 2A 90 7A 0C 7D 32 A3 5E E5 BD BC B8 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 97 69 37 89"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 4E CD 35 C4 05 E0 5B C4 16 15 91 41 00 00 00 00 20 51 FA BA 04 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 00 00 00 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 78 E4 00 00 75 6C 04 00 D8 E0 6F 00 B7 D4 6F 00 46 5F 1A 00 0C 63 A9 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Peugeout 206": [
        {"off": 0x5870, "hex": "35 B2 44 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 13 E5 B2 72 4D 71 78 52 AC 58 A8 A3 ED 76 E8 5F 00 00 00 00 00 00 00 00 87 32 5F C3 3E 4E B0 C1 85 E2 70 0B 65 BE 2A AD 23 7E 62 C3 CD 28 8D 30 26 07 77 30 97 BE 66 36 0F BD E4 1E 43 AE 8C 01 96 B6 EF 0F 9B CA DD 12 57 34 DE C1 CA 86 13 FE 26 75 87 03 79 E1 E4 74 4A 08 54 56 1D D9 43 21 00 00 00 00 00 00 00 00 00 73 C7 D8 2A F5 F5 47 46 DC 6F F5 46 DC 6F F5 56 73 E6 F6 56 73 E6 F6 00 00 00 00 A8 3D 32 E7 68 8E A3 53 3E E2 8F 46 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 E1 72 FD 9E D2 4F 95 0D 73 D9 F3 FC 15 A8 89 A4 A8 6E 70 91 25 98 A9 81 D8 39 B3 79 6E A3 7E 8F 21 D5 04 DB DE 80 F1 81 B1 39 F8 82 E5 2E 39 2D 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 4B CD 10 4B"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 AD 33 35 C4 73 E0 5B C4 38 08 92 41 00 00 00 00 20 51 A4 8D D6 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 B7 99 72 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 79 EA 00 00 62 EE 04 00 29 C3 68 00 75 F0 78 00 BE 79 02 00 D4 4D D7 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Volkswagen Golf": [
        {"off": 0x5870, "hex": "C9 2B 51 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 87 30 16 00 41 05 39 B7 A0 C7 82 FC 61 D7 F6 D6 00 00 00 00 00 00 00 00 7B ED 83 C7 B2 67 6C 4A 85 E2 70 0B D9 A3 6E 89 17 39 87 C7 41 42 49 B9 9A 20 33 B9 0B 05 8F DE 03 05 24 BF B7 61 E0 54 8A D8 B9 CD 0F 11 06 BB CB E7 31 15 BE A8 DD BB 9A EF F8 22 6D AA 85 82 3E 04 86 4F 91 53 B5 40 00 00 00 00 00 00 00 00 F4 94 91 96 9E 55 04 BF BA 3C 7E 6C BA 3C 7E 6C CA D3 F4 6D CA D3 F4 6D 00 00 00 00 1C 9E 40 5E 68 8E A3 53 B2 42 9E BD 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 D5 3B 9E AC C6 CC 19 FA E7 87 A2 13 89 29 12 F7 9C 1E 09 35 19 15 2E 6E 4C 55 C7 F6 E2 6B 07 A2 15 AC A6 3E D2 E4 64 55 25 1C D8 C4 4F F9 6E 3C 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 FA 26 AF 42"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 A9 32 35 C4 62 E0 5B C4 16 63 92 41 00 00 00 00 20 51 90 DA D4 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 B7 99 72 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 14 1E 06 00 C2 A9 04 00 88 EB 7E 00 D7 0D 77 00 9B 51 10 00 CB 9A C1 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Audi TT": [
        {"off": 0x5870, "hex": "A0 C7 84 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 E7 06 00 00 A1 D7 A7 20 00 42 42 21 C1 85 80 8A 00 00 00 00 00 00 00 00 DB 07 1F 2F 12 CE 6A A5 85 E2 70 0B 39 AA 1C 7D 77 53 22 2F A1 A8 47 14 FA 86 31 14 6B 83 C0 F2 63 37 EF 79 17 F8 6A 3B EA 3A 97 85 6F 8F 37 CF 2B 7E BC FB 1E 0B BB 73 FA CD 72 C6 CD 54 3B 95 9E 96 0D A2 F1 31 2F E4 00 00 00 00 00 00 00 00 54 F7 6E 4E FE 03 8E 72 1A EB 07 20 1A EB 07 20 2A 82 7E 21 2A 82 7E 21 00 00 00 00 7C 4C CA 11 68 8E A3 53 12 F1 27 71 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 35 E6 53 BF 26 D7 83 43 47 C6 C4 B8 E9 4F D1 6F FC 10 AD C5 79 1F 98 B7 AC AB 72 6D 42 DA E1 70 75 E6 CE E8 32 37 85 2A 85 BA 02 3E 4F F9 6E 3C 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 78 AD B9 AF"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 6E 62 35 C4 40 21 5B C4 0C 9A 91 41 00 00 00 00 20 51 76 A3 D4 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 B7 99 72 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 23 0F 03 00 D1 9A 44 00 08 3D 7D 00 57 5F 75 00 E9 93 05 00 19 BE B6 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Audi A3 (TEST)": [
        {"off": 0x5870, "hex": "6F FC 89 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 53 04 00 00 8D 18 1B 1D EC AF 3E CC 2D E6 70 97 00 00 00 00 00 00 00 00 C7 49 B2 FB 7E 4D 66 04 85 E2 70 0B A5 7D 75 4E 63 95 B5 FB 0D 5A 43 73 66 06 2D 73 D7 8D 99 FE 4F A4 5A B8 83 4D B0 A1 D6 3D 87 B4 DB 99 10 DB 97 D3 01 62 0A 0E AB A2 66 84 35 9C B9 D8 54 23 8A 2F DD FD 5D E8 F1 B9 00 00 00 00 00 00 00 00 40 FA 5E 7D 6A 64 7E 7F 86 4B F8 2C 86 4B F8 2C 96 E2 6E 2E 96 E2 6E 2E 00 00 00 00 E8 AC BA 1E 68 8E A3 53 7E 51 18 7E 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 21 6A 6D 4D 12 87 28 EB B3 28 5D CD 55 27 D6 6F E8 D5 4C C6 65 CF 3C 5F 18 59 AD 09 AE 92 7D 06 61 AC E1 31 1E 28 61 03 F1 C8 5C 32 B1 43 EE 98 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 8B A4 60 02"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 32 32 35 C4 5C E0 5B C4 AA 2F 92 41 00 00 00 00 20 51 D1 C9 D4 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 B7 99 72 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 54 21 06 00 02 AD 04 00 B0 68 7E 00 FF 8A 76 00 17 C6 0D 00 47 F0 BE 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Hyundai Tiburon GT": [
        {"off": 0x5870, "hex": "34 82 4F 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 22 05 FD 04 BC F2 13 AB 5B 30 CA 39 BC 94 46 AA 00 00 00 00 00 00 00 00 36 CB 57 5D CD FC BB 9A 85 E2 70 0B F4 4D 94 98 D2 16 5B 5D 5C D7 98 09 B5 B5 82 09 E6 4C 18 81 7E 3D 66 19 52 0C DB BE 85 D6 09 77 EA 58 8F 5D 66 92 2C 7F B9 A6 2D 65 75 E2 4D 68 A8 F8 78 72 B9 87 4A FC 6C 46 0A 86 00 00 00 00 00 00 00 00 EF 92 E1 3F F9 12 54 92 15 FA CD 3F 15 FA CD 3F 25 91 44 41 25 91 44 41 00 00 00 00 77 5B 90 31 68 8E A3 53 0D 00 EE 90 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 10 8A 91 9C 01 26 29 F0 C2 25 3E B6 A4 94 E6 52 17 ED 6A 0B 54 6E 3D 64 E7 D5 C1 AE 3D 7F A4 42 D0 2A E6 F2 4D FE 7E 17 00 65 35 CA 3A DB AF 9E 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 FA 26 AF 42"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 AD 33 35 C4 73 E0 5B C4 6D 96 92 41 00 00 00 00 20 51 7D FF D4 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 B7 99 72 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 40 A0 00 00 EE 2B 04 00 00 0C 80 00 4F 2E 78 00 30 61 25 00 60 8B D6 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Pontiac GTO": [
        {"off": 0x5870, "hex": "89 82 97 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 C9 AC 00 00 C3 7A 05 13 A2 B8 BD 9C 23 B0 36 6F 00 00 00 00 00 00 00 00 7D FC 26 41 F4 56 71 F8 85 E2 70 0B 1B 71 E1 36 19 48 2A 41 83 31 4E 67 DC 0F 38 67 CD CC 8C 21 85 DC C6 2D F9 21 6F 4E 0C A1 20 F9 D1 D8 03 FE 0D A8 C0 0E 40 71 44 E7 5C 59 1B 15 6F 4C F5 B8 C0 3D 41 EA 53 BD D7 32 00 00 00 00 00 00 00 00 76 5D F8 C1 60 2E 44 57 7C 15 BE 04 7C 15 BE 04 8C AC 34 06 8C AC 34 06 00 00 00 00 DE 76 80 F6 68 8E A3 53 74 1B DE 55 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 D7 DD 0D E3 C8 50 04 D8 A9 93 6B 58 CB 5C 41 73 1E BA 1E 37 1B 99 18 4C 8E 59 02 92 A4 88 14 F8 17 61 57 56 54 E2 16 1C E7 C9 C9 61 E5 BD BC B8 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 41 01 C1 5E"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 4E CD 35 C4 05 E0 5B C4 02 DB 91 41 00 00 00 00 20 51 9F 0C D3 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 00 00 00 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 D9 70 00 00 D6 F8 41 00 98 D2 70 00 77 C6 70 00 5B 83 20 00 21 87 AF 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Mazda RX7 (TEST)": [
        {"off": 0x5870, "hex": "6E 4E 98 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 00 DC 00 00 5A C4 C6 35 79 7E AC AA 1A 97 2A 86 00 00 00 00 00 00 00 00 54 DB 94 73 AB 10 9B 78 85 E2 70 0B D2 63 44 8D F0 26 98 73 3A EB 77 E7 93 C9 61 E7 44 D0 0B 53 1C CD 27 B3 30 DF BC DB 23 05 26 30 48 DC 82 2F 44 65 0E 9C 57 D5 49 1E D3 E3 C5 F0 C6 25 F1 09 57 D5 F8 2E CA 47 82 0E 00 00 00 00 00 00 00 00 8D C1 FD F8 57 15 F6 6E 73 FC B2 1C 73 FC B2 1C 83 93 28 1D 83 93 28 1D 00 00 00 00 D5 5D 74 0E 68 8E A3 53 6B 02 90 6D 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 2E B7 09 34 1F 91 13 06 20 A5 D8 78 82 A4 7D 93 B5 F8 E3 5E 72 D9 27 7A C5 A4 F9 81 9B 7D 0B C3 EE F4 2C 80 EB C7 A0 11 5E 62 90 08 AA 9A CD ED 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 18 F9 A4 78"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 4E CD 35 C4 05 E0 5B C4 DF 5A 92 41 00 00 00 00 20 51 85 CF 04 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 00 00 00 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 8C C2 00 00 89 4A 04 00 40 F5 20 00 1F E9 20 00 D2 27 12 00 98 2B A1 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Mazda RX8": [
        {"off": 0x5870, "hex": "C7 44 8D 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 01 DC 00 00 FB EC 1B 38 DA AC D3 76 5B FD C2 37 00 00 00 00 00 00 00 00 B5 38 88 A4 2C 1A FA C7 85 E2 70 0B 53 7C 56 8D 51 84 8B A4 BB F4 D6 36 14 D3 C0 36 05 3E 53 F6 BD 06 68 EE 31 C1 96 6E 44 27 3C 1E 09 4A CA D2 45 47 E8 2E 78 F7 5F 0C 94 82 FB B8 A7 9C DA D8 F8 1F A5 A1 8B E6 B7 D6 00 00 00 00 00 00 00 00 AE E3 13 E7 98 7B D0 1F B4 62 4A CD B4 62 4A CD C4 F9 C0 CE C4 F9 C0 CE 00 00 00 00 16 C4 0C BF 68 8E A3 53 AC 68 6A 1E 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 0F 2E F3 02 00 59 72 6B E1 74 9D 45 03 90 99 69 56 54 7D F8 53 A1 86 DF C6 68 31 93 DC 45 44 01 4F C5 7E 85 8C 34 A8 B2 1F 63 85 CA E6 BD BC B8 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 79 85 A5 78"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 6E 62 35 C4 40 21 5B C4 8D B9 91 41 00 00 00 00 20 51 87 48 D4 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 B7 D4 6F 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 C4 BA 00 00 F6 DD 41 00 A0 76 7A 00 B7 99 72 00 2F 25 42 00 3E 01 B4 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Mazda Miata MX5": [
        {"off": 0x5870, "hex": "40 C9 33 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 6B 5D 45 03 A5 E0 9B C6 04 C2 2F 32 45 15 FC 6B 00 00 00 00 00 00 00 00 DF C3 1E 7C 96 0A 62 92 85 E2 70 0B BD A2 71 B8 7B 0F 22 7C 25 E5 3E 01 7E C3 28 01 EF F0 78 FA 67 04 CE 05 9B D6 F4 12 EE E9 5C 4E F3 FC EF D6 AF 5C 46 D3 22 BA 80 3C 7E 7F 72 12 D1 36 31 61 A2 27 5B A4 75 E3 2E 30 00 00 00 00 00 00 00 00 58 A6 34 17 82 93 09 54 9E 7A 83 01 9E 7A 83 01 AE 11 FA 02 AE 11 FA 02 00 00 00 00 00 DC 45 F3 68 8E A3 53 96 80 A3 52 05 47 C9 FA 05 47 C9 FA AD 09 64 45 AD 09 64 45 97 4E 44 FA 97 4E 44 FA 05 47 C9 FA 05 47 C9 FA 05 47 C9 FA 05 47 C9 FA AD 09 64 45 AD 09 64 45 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 39 C8 49 8B 2A 7D 2D E2 CB BB 0F AE 6D 14 19 34 00 66 ED 12 7D C5 41 56 30 12 51 E1 C6 F1 F3 55 79 EE 23 70 36 50 3C DB 09 F4 9C 05 8A 9A CD ED 00 00 00 00 00 00 00 00"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 D7 DD 0D E3 C8 50 04 D8 A9 93 6B 58 CB 5C 41 73 1E BA 1E 37 1B 99 18 4C 8E 59 02 92 A4 88 14 F8 17 61 57 56 54 E2 16 1C E7 C9 C9 61 E5 BD BC B8 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 A3 86 60 2C"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 4D 32 35 C4 6A E0 5B C4 1E 38 92 41 00 00 00 00 20 51 70 39 D5 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 00 00 00 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 C2 C5 00 00 17 D6 04 00 B8 D0 81 00 37 F2 79 00 5B 1D 08 00 B2 6A E0 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],
    "Lexus IS 300 (BETA)": [
        {"off": 0x5870, "hex": "15 0E 6A 43 01 00 00 00 04 00 00 00 01 00 00 00 00 00 00 00 EE 36 02 03 08 24 DC 5C A7 B6 C8 8E 88 81 27 E3 00 00 00 00 00 00 00 00 82 C5 0A 05 99 40 CE 38 85 E2 70 0B C0 85 35 96 1E 11 0E 05 28 1B AB A7 81 F9 94 A7 B2 B3 CA EC CA FA C0 79 1E 56 C2 E0 D1 59 DA D5 B6 BF 41 C9 32 DC 13 A1 05 2A FE C3 41 55 30 CE F4 C4 A9 94 05 D1 03 8B 38 B9 EC EB 00 00 00 00 00 00 00 00 3B 16 B2 9E C5 FF 34 CB E1 E6 AE 78 E1 E6 AE 78 F1 7D 25 7A F1 7D 25 7A 00 00 00 00 43 48 71 6A 68 8E A3 53 D9 EC CE C9 05 47 C9 FA 05 47 C9 FA AD 09 64 45"},
        {"off": 0x5950, "hex": "00 00 00 00 00 00 00 00 5C 56 C2 BE 4D 7E 57 01 8E A4 9C 1B 70 F0 BE E0 63 C2 4E 54 A0 C6 6B 75 B3 37 BB E5 09 84 7D 1D 1C C9 DF 28 99 5F 59 B2 CC EF 5B C0 0B 2F BC B8 00 00 00 00 00 00 00 00"},
        {"off": 0x5B20, "hex": "20 E8 F9 03 00 00 00 00 00 00 00 00 46 95 E2 59"},
        {"off": 0xAD80, "hex": "8C 9A 31 01 A3 32 35 C4 68 E0 5B C4 18 D3 91 41 00 00 00 00 20 51 A0 E7 D4 44 01 00 00 00 00 00"},
        {"off": 0xC2D0, "hex": "00 00 00 B7 99 72 00 00 01 01 01 00 00 00 00 00"},
        {"off": 0xC3B0, "hex": "00 00 00 00 00 00 00 00 00 00 00 F2 F2 00 00 A0 7E 04 00 90 51 7F 00 DF 73 77 00 96 96 1B 00 C6 C0 CC 00 00 00 00 00 00 00 00 00 00 00 00 00 00"}
    ],

}

class NFSU2App:
    def __init__(self, root):
        self.root = root
        self.cur_lang = 'IT'
        self.all_saves = {}
        
        # Carica Icona
        try: self.root.iconbitmap(self.get_path("icona.ico"))
        except: pass

        self.setup_ui()
        self.full_scan()

    def get_path(self, rel):
        if hasattr(sys, '_MEIPASS'): return os.path.join(sys._MEIPASS, rel)
        return os.path.join(os.path.abspath("."), rel)

    def setup_ui(self):
        self.root.title(LANG[self.cur_lang]['title'])
        self.root.geometry("480x940")
        self.root.configure(bg="#0f0f0f")

        # Selettore Lingua in alto a destra
        lang_frame = tk.Frame(self.root, bg="#0f0f0f")
        lang_frame.pack(anchor="ne", padx=10, pady=5)
        tk.Button(lang_frame, text="IT", command=lambda: self.change_lang('IT'), bg="#333", fg="white", font=("Arial", 8)).pack(side="left", padx=2)
        tk.Button(lang_frame, text="EN", command=lambda: self.change_lang('EN'), bg="#333", fg="white", font=("Arial", 8)).pack(side="left", padx=2)

        # Immagine Header
        try:
            img = Image.open(self.get_path("header.png")).resize((420, 180))
            self.header_img = ImageTk.PhotoImage(img)
            tk.Label(self.root, image=self.header_img, bg="#0f0f0f").pack(pady=5)
        except:
            tk.Label(self.root, text="NFSU2 MASTER", fg="#00FF41", bg="#0f0f0f", font=("Impact", 28)).pack(pady=10)

        # UI Components con refresh dinamico
        self.lbl_profiles = tk.Label(self.root, text=LANG[self.cur_lang]['profiles'], fg="#00FF41", bg="#0f0f0f", font=("bold", 9))
        self.lbl_profiles.pack()
        
        self.listbox = tk.Listbox(self.root, bg="#1a1a1a", fg="#00FF41", font=("Consolas", 11), height=8)
        self.listbox.pack(pady=5, padx=30, fill="x")

        self.lbl_car = tk.Label(self.root, text=LANG[self.cur_lang]['select_car'], fg="white", bg="#0f0f0f")
        self.lbl_car.pack()
        
        self.car_cb = ttk.Combobox(self.root, values=list(CAR_DATABASE.keys()), state="readonly")
        self.car_cb.pack(pady=5, padx=60, fill="x")
        if list(CAR_DATABASE.keys()): self.car_cb.set(list(CAR_DATABASE.keys())[0])

        self.btn_inject = self.add_btn(LANG[self.cur_lang]['inject_btn'], self.apply_car, "#C0392B", "white")
        
        self.lbl_money = tk.Label(self.root, text=LANG[self.cur_lang]['money'], fg="white", bg="#0f0f0f")
        self.lbl_money.pack(pady=5)
        
        self.money_entry = tk.Entry(self.root, justify="center", bg="#1a1a1a", fg="#00FF41", font=("Consolas", 20))
        self.money_entry.insert(0, "999999")
        self.money_entry.pack(pady=5, padx=100, fill="x")

        self.btn_patch = self.add_btn(LANG[self.cur_lang]['patch_btn'], self.apply_money, "#00FF41", "black")
        self.btn_rename = self.add_btn(LANG[self.cur_lang]['rename_btn'], self.apply_rename, "white", "black")
        self.btn_backup = self.add_btn(LANG[self.cur_lang]['backup_btn'], self.apply_backup, "#2980B9", "white")

        self.lbl_footer = tk.Label(self.root, text=LANG[self.cur_lang]['footer'], fg="#555", bg="#0f0f0f", font=("Arial", 8))
        self.lbl_footer.pack(side="bottom", pady=10)

    def add_btn(self, text, command, bg, fg):
        btn = tk.Button(self.root, text=text, command=command, bg=bg, fg=fg, font=("Arial", 10, "bold"), relief="flat", pady=7)
        btn.pack(pady=4, padx=50, fill="x")
        return btn

    def change_lang(self, lang_code):
        self.cur_lang = lang_code
        self.root.title(LANG[lang_code]['title'])
        self.lbl_profiles.config(text=LANG[lang_code]['profiles'])
        self.lbl_car.config(text=LANG[lang_code]['select_car'])
        self.btn_inject.config(text=LANG[lang_code]['inject_btn'])
        self.lbl_money.config(text=LANG[lang_code]['money'])
        self.btn_patch.config(text=LANG[lang_code]['patch_btn'])
        self.btn_rename.config(text=LANG[lang_code]['rename_btn'])
        self.btn_backup.config(text=LANG[lang_code]['backup_btn'])
        self.lbl_footer.config(text=LANG[lang_code]['footer'])

    def full_scan(self):
        self.listbox.delete(0, tk.END)
        path = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'NFS Underground 2')
        if os.path.exists(path):
            for d in os.listdir(path):
                p = os.path.join(path, d, d)
                if os.path.exists(p):
                    self.all_saves[d] = p
                    self.listbox.insert(tk.END, d)

    def apply_car(self):
        idx = self.listbox.curselection()
        if not idx: return messagebox.showwarning("!", LANG[self.cur_lang]['err_select'])
        path = self.all_saves[self.listbox.get(idx)]
        car = self.car_cb.get()
        try:
            with open(path, "rb+") as f:
                for block in CAR_DATABASE[car]:
                    f.seek(block["off"])
                    f.write(bytes.fromhex(block["hex"].replace(" ", "")))
            messagebox.showinfo("OK", LANG[self.cur_lang]['success_inject'])
        except Exception as e: messagebox.showerror("Err", str(e))

    def apply_money(self):
        idx = self.listbox.curselection()
        if not idx: return
        path = self.all_saves[self.listbox.get(idx)]
        with open(path, "rb+") as f:
            f.seek(41322)
            f.write(struct.pack("<I", int(self.money_entry.get())))
        messagebox.showinfo("OK", LANG[self.cur_lang]['success_money'])

    def apply_rename(self):
        idx = self.listbox.curselection()
        if not idx: return
        old_name = self.listbox.get(idx)
        new_name = simpledialog.askstring("Rename", LANG[self.cur_lang]['rename_prompt'])
        if not new_name: return
        new_name = new_name.strip()[:7]
        path = self.all_saves[old_name]
        try:
            with open(path, "rb+") as f:
                f.seek(0xD220 + 5)
                f.write(new_name.encode().ljust(7, b'\x00'))
            
            old_dir = os.path.dirname(path)
            parent = os.path.dirname(old_dir)
            new_file_path = os.path.join(old_dir, new_name)
            os.rename(path, new_file_path)
            os.rename(old_dir, os.path.join(parent, new_name))
            
            self.full_scan()
            messagebox.showinfo("OK", LANG[self.cur_lang]['success_rename'])
        except Exception: messagebox.showerror("Err", LANG[self.cur_lang]['err_admin'])

    def apply_backup(self):
        idx = self.listbox.curselection()
        if not idx: return
        src = self.all_saves[self.listbox.get(idx)]
        dst = os.path.join(os.path.expanduser("~"), "Desktop", "NFSU2_Backups")
        os.makedirs(dst, exist_ok=True)
        shutil.copy2(src, os.path.join(dst, os.path.basename(src) + f"_{self.listbox.get(idx)}.bak"))
        messagebox.showinfo("OK", "Backup Saved!")

if __name__ == "__main__":
    root = tk.Tk()
    app = NFSU2App(root)
    root.mainloop()