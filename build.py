import os
import shutil
import zipfile
import json
import subprocess
import sys

# Configurações
APP_NAME = "HeAVY"
VERSION = "1.2.0"
AUTHOR = "Havylliard"
MAIN_FILE = "HeAVY.py"
ASSETS_DIR = "assets"

def build():
    print(f"--- Iniciando Build {APP_NAME} v{VERSION} ---")

    # Verifica se os arquivos necessários existem na pasta atual
    if not os.path.exists(MAIN_FILE):
        print(f"ERRO: {MAIN_FILE} não encontrado na pasta atual!")
        return

    # 1. Gerar o Executável
    print("Gerando executável... Isso pode demorar um pouco.")
    try:
        # Usamos sys.executable para garantir que usamos o mesmo Python que está rodando este script
        subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--noconsole",
            "--onefile",
            f"--add-data={ASSETS_DIR}{os.pathsep}{ASSETS_DIR}",
            "--name", f"{APP_NAME}-{VERSION}",
            MAIN_FILE
        ], check=True)
    except subprocess.CalledProcessError:
        print("ERRO ao compilar. Verifique se instalou o pyinstaller: pip install pyinstaller")
        return

    # 2. Pastas
    dist_folder = "dist"
    release_folder = "release_final"
    if os.path.exists(release_folder):
        shutil.rmtree(release_folder)
    os.makedirs(release_folder)

    # 3. Copiar o EXE gerado
    exe_name = f"{APP_NAME}-{VERSION}.exe"
    shutil.copy(os.path.join(dist_folder, exe_name), release_folder)

    # 4. Criar o manifest.json
    print("Criando manifest.json...")
    manifest = {
        "manifestType": "minecraftModpack",
        "manifestVersion": 1,
        "name": f"{APP_NAME} - Hytale Advanced Versatile Yield",
        "version": VERSION,
        "author": AUTHOR,
        "description": "Ferramenta avançada para gestão de chunks e recuperação de mundos no Hytale.",
        "files": [],
        "overrides": "overrides"
    }
    
    with open(os.path.join(release_folder, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # 5. Criar o ZIP para o CurseForge
    zip_name = f"{APP_NAME}_v{VERSION}_CurseForge.zip"
    print(f"Criando pacote final: {zip_name}")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, release_folder))

    # Limpeza de pastas temporárias (opcional)
    # shutil.rmtree(release_folder)
    print(f"\n--- PRONTO! O arquivo para upload é: {zip_name} ---")

if __name__ == "__main__":
    build()