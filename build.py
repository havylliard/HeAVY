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
        self.root.title(f"{APP_NAME} Tool Builder - v{AUTHOR}")
        self.root.geometry("500x400")
        
        # Interface
        self.label = tk.Label(root, text="Preparado para iniciar o Build", font=("Arial", 10, "bold"))
        self.label.pack(pady=10)

        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        self.status_text = tk.Text(root, height=10, width=55, state="disabled", font=("Consolas", 9))
        self.status_text.pack(pady=10)

        self.btn_build = tk.Button(root, text="🚀 Iniciar Build e Subir", command=self.start_thread, bg="#4CAF50", fg="white", width=20)
        self.btn_build.pack(side="left", padx=20, pady=10)

        self.btn_clean = tk.Button(root, text="🧹 Limpar Pastas", command=self.clean_folders, width=20)
        self.btn_clean.pack(side="right", padx=20, pady=10)

    def log(self, message):
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, f"> {message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state="disabled")
        self.root.update_idletasks()

    def get_version(self):
        try:
            with open(UPDATE_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                last_line = lines[-1].strip()
                # Pega o que está entre 'v' e o hífen '-' (ex: v 1.2.2 - texto -> 1.2.2)
                version = last_line.split('-')[0].replace('v', '').strip()
                return version
        except Exception as e:
            self.log(f"Erro ao ler versão: {e}")
            return "1.0.0"

    def clean_folders(self):
        folders = ["build", "dist", "release_final"]
        for f in folders:
            if os.path.exists(f):
                shutil.rmtree(f)
        self.log("Pastas temporárias limpas.")
        messagebox.showinfo("Limpeza", "Pastas build, dist e release limpas!")

    def start_thread(self):
        Thread(target=self.run_build).start()

    def run_build(self):
        version = self.get_version()
        self.log(f"Versão detectada: {version}")
        self.progress['value'] = 10
        
        # 1. Mover Zips antigos
        if not os.path.exists(BUILDS_HISTORY_DIR):
            os.makedirs(BUILDS_HISTORY_DIR)
        for item in os.listdir("."):
            if item.endswith(".zip") and item.startswith(APP_NAME):
                shutil.move(item, os.path.join(BUILDS_HISTORY_DIR, item))
        self.log("Zips antigos movidos para Heavy-Buids.")
        self.progress['value'] = 20

        # 2. Gerar EXE
        self.log("Compilando Executável (PyInstaller)...")
        exe_name = f"{APP_NAME}-{version}"
        try:
            subprocess.run([
                sys.executable, "-m", "PyInstaller", "--noconfirm", "--onefile", "--windowed",
                f"--add-data={ASSETS_DIR}{os.pathsep}{ASSETS_DIR}",
                f"--icon={ICON_PATH}", "--name", exe_name, MAIN_FILE
            ], check=True, capture_output=True)
        except Exception as e:
            self.log(f"Erro no PyInstaller: {e}")
            return
        self.progress['value'] = 60

        # 3. Criar Manifest e Pasta Release
        release_path = "release_final"
        if os.path.exists(release_path): shutil.rmtree(release_path)
        os.makedirs(release_path)
        
        shutil.copy(f"dist/{exe_name}.exe", release_path)
        
        manifest = {
            "manifestType": "minecraftModpack", "manifestVersion": 1,
            "name": f"{APP_NAME} - Hytale Tool", "version": version,
            "author": AUTHOR, "files": [{"fileName": f"{exe_name}.exe"}]
        }
        with open(f"{release_path}/manifest.json", "w") as f:
            json.dump(manifest, f, indent=4)
        
        self.log("Manifest.json criado.")
        self.progress['value'] = 80

        # 4. Zipar
        zip_final = f"{APP_NAME}_v{version}_By{AUTHOR}.zip"
        with zipfile.ZipFile(zip_final, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in os.listdir(release_path):
                zipf.write(os.path.join(release_path, file), file)
        
        # Copia o zip final para a raiz também como solicitado
        shutil.copy(zip_final, f"dist/{zip_final}")
        
        self.log(f"Pacote {zip_final} gerado com sucesso!")
        self.progress['value'] = 90

        # 5. GitHub e CurseForge
        self.log("Subindo para o GitHub...")
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"Build v{version}"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            self.log("GitHub atualizado!")
        except:
            self.log("Falha ao subir Git (Verifique se há mudanças).")

        self.progress['value'] = 100
        self.log("--- PROCESSO FINALIZADO ---")
        
        if messagebox.askyesno("Sucesso", "Build pronto e Git atualizado! Abrir CurseForge agora?"):
            webbrowser.open(CURSEFORGE_URL)

if __name__ == "__main__":
    root = tk.Tk()
    app = BuilderApp(root)
    root.mainloop()