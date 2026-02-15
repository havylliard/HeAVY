import os
import shutil
import zipfile
import json
import subprocess
import sys
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
import time

# --- CONFIGURAÇÕES ---
APP_NAME = "HeAVY"
AUTHOR = "Havylliard"
MAIN_FILE = "HeAVY.py"
UPDATE_FILE = "update.txt"
ASSETS_DIR = "assets"
ICON_PATH = os.path.join("assets", "imgs", "heavy.ico")
BUILDS_HISTORY_DIR = "Heavy-Buids"
CURSEFORGE_URL = "https://authors.curseforge.com/#/projects/1462651/files"

class BuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"🛠️ {APP_NAME} - Professional Builder v1.2")
        self.root.geometry("600x600")
        self.root.configure(bg="#0f0f0f") # Fundo quase preto

        # Estilo da Barra de Progresso
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("green.Horizontal.TProgressbar", background='#00ff00', troughcolor='#1e1e1e', bordercolor='#0f0f0f', lightcolor='#00ff00', darkcolor='#00ff00')

        # Título
        tk.Label(root, text="HeAVY BUILD SYSTEM", font=("Segoe UI", 16, "bold"), bg="#0f0f0f", fg="#00ff00").pack(pady=15)
        
        # Container de Status
        self.frame_status = tk.Frame(root, bg="#1e1e1e", bd=2, relief="flat")
        self.frame_status.pack(padx=20, pady=5, fill="both", expand=True)

        self.status_text = tk.Text(self.frame_status, height=15, width=70, state="disabled", font=("Consolas", 10), bg="#1e1e1e", fg="#00ff00", insertbackground="white", padx=10, pady=10)
        self.status_text.pack(fill="both", expand=True)

        # Labels de Checkpoint (Visual de Menu)
        self.check_frame = tk.Frame(root, bg="#0f0f0f")
        self.check_frame.pack(pady=10)
        
        self.checks = {
            "version": tk.Label(self.check_frame, text="[ ] Identificar Versão", bg="#0f0f0f", fg="#555", font=("Consolas", 9)),
            "clean": tk.Label(self.check_frame, text="[ ] Limpeza de Pastas", bg="#0f0f0f", fg="#555", font=("Consolas", 9)),
            "pyinstaller": tk.Label(self.check_frame, text="[ ] Compilar Executável", bg="#0f0f0f", fg="#555", font=("Consolas", 9)),
            "zip": tk.Label(self.check_frame, text="[ ] Gerar Pacote ZIP", bg="#0f0f0f", fg="#555", font=("Consolas", 9)),
            "git": tk.Label(self.check_frame, text="[ ] Subir para GitHub", bg="#0f0f0f", fg="#555", font=("Consolas", 9))
        }
        for c in self.checks.values(): c.pack(anchor="w")

        # Barra de Progresso
        self.progress = ttk.Progressbar(root, orient="horizontal", length=540, mode="determinate", style="green.Horizontal.TProgressbar")
        self.progress.pack(pady=15)

        # Botões
        self.btn_frame = tk.Frame(root, bg="#0f0f0f")
        self.btn_frame.pack(pady=15)

        self.btn_build = tk.Button(self.btn_frame, text="🚀 START COMPILATION", command=self.start_thread, bg="#008000", fg="white", font=("Segoe UI", 10, "bold"), width=22, relief="flat", cursor="hand2")
        self.btn_build.pack(side="left", padx=10)

        self.btn_clean = tk.Button(self.btn_frame, text="🧹 RESET SYSTEM", command=self.clean_folders, bg="#800000", fg="white", font=("Segoe UI", 10, "bold"), width=22, relief="flat", cursor="hand2")
        self.btn_clean.pack(side="right", padx=10)

    def log(self, message, type="INFO"):
        prefix = ">>" if type == "INFO" else "!!"
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, f"{prefix} {message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state="disabled")
        self.root.update_idletasks()

    def set_check(self, key, status="done"):
        color = "#00ff00" if status == "done" else "#ffcc00"
        symbol = "[✅]" if status == "done" else "[⏳]"
        text = self.checks[key].cget("text")[4:]
        self.checks[key].config(text=f"{symbol} {text}", fg=color)

    def get_version(self):
        try:
            with open(UPDATE_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                last_line = lines[-1].strip()
                version = last_line.split('-')[0].replace('v', '').strip()
                return version
        except: return "1.0.0"

    def clean_folders(self):
        self.log("Limpando arquivos temporários...")
        folders = ["build", "dist", "release_final", "__pycache__"]
        for f in folders:
            if os.path.exists(f):
                shutil.rmtree(f, ignore_errors=True)
        for item in os.listdir("."):
            if item.endswith(".spec"): os.remove(item)
        self.log("Sistema resetado.")
        messagebox.showinfo("Reset", "Pastas limpas!")

    def start_thread(self):
        self.btn_build.config(state="disabled")
        Thread(target=self.run_build).start()

    def run_build(self):
        # Passo 1: Versão
        self.set_check("version", "work")
        version = self.get_version()
        self.log(f"Versão lida do update.txt: v{version}")
        self.progress['value'] = 10
        time.sleep(1)
        self.set_check("version", "done")

        # Passo 2: Limpeza
        self.set_check("clean", "work")
        self.log("Removendo builds anteriores...")
        self.clean_folders()
        if not os.path.exists(BUILDS_HISTORY_DIR): os.makedirs(BUILDS_HISTORY_DIR)
        for item in os.listdir("."):
            if item.endswith(".zip") and item.startswith(APP_NAME):
                shutil.move(item, os.path.join(BUILDS_HISTORY_DIR, item))
        self.progress['value'] = 25
        self.set_check("clean", "done")

        # Passo 3: PyInstaller
        self.set_check("pyinstaller", "work")
        self.log("Iniciando PyInstaller... (Isso pode demorar)")
        exe_name = f"{APP_NAME}-{version}"
        try:
            # Comando com ícone
            process = subprocess.run([
                sys.executable, "-m", "PyInstaller", "--noconfirm", "--onefile", "--windowed",
                f"--add-data={ASSETS_DIR}{os.pathsep}{ASSETS_DIR}",
                f"--icon={ICON_PATH}", "--name", exe_name, MAIN_FILE
            ], capture_output=True, text=True)
            if process.returncode != 0:
                self.log(f"Erro na compilação: {process.stderr}", "ERROR")
                return
        except Exception as e:
            self.log(f"Falha crítica: {e}", "ERROR")
            return
        self.progress['value'] = 60
        self.set_check("pyinstaller", "done")

        # Passo 4: ZIP e Manifest
        self.set_check("zip", "work")
        self.log("Gerando manifest.json e empacotando...")
        release_path = "release_final"
        os.makedirs(release_path, exist_ok=True)
        shutil.copy(f"dist/{exe_name}.exe", release_path)
        
        manifest = {
            "manifestType": "minecraftModpack", "manifestVersion": 1,
            "name": f"{APP_NAME} - Hytale Tool", "version": version,
            "author": AUTHOR, "files": [{"fileName": f"{exe_name}.exe"}]
        }
        with open(f"{release_path}/manifest.json", "w") as f:
            json.dump(manifest, f, indent=4)
        
        zip_final = f"{APP_NAME}_v{version}_By{AUTHOR}.zip"
        with zipfile.ZipFile(zip_final, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in os.listdir(release_path):
                zipf.write(os.path.join(release_path, file), file)
        
        shutil.copy(zip_final, f"dist/{zip_final}")
        self.log(f"Pacote gerado: {zip_final}")
        self.progress['value'] = 85
        self.set_check("zip", "done")

        # Passo 5: Git
        self.set_check("git", "work")
        self.log("Sincronizando com repositório remoto...")
        try:
            subprocess.run(["git", "add", MAIN_FILE, ASSETS_DIR, UPDATE_FILE, "README.md", "build.py", zip_final], check=True)
            subprocess.run(["git", "commit", "-m", f"Build v{version}"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            self.log("GitHub atualizado com sucesso!")
        except:
            self.log("Git: Nada para atualizar.")
        
        self.progress['value'] = 100
        self.set_check("git", "done")
        self.log("TRABALHO FINALIZADO COM SUCESSO!", "INFO")
        
        self.btn_build.config(state="normal")
        if messagebox.askyesno("Finalizado", "Tudo pronto! Abrir CurseForge agora?"):
            webbrowser.open(CURSEFORGE_URL)

if __name__ == "__main__":
    root = tk.Tk()
    app = BuilderApp(root)
    root.mainloop()