import sys
import os
import subprocess
import time
import zipfile
import shutil

# Diretório base do Minecraft dentro do ecossistema Waydroid
MINECRAFT_DIR = "/home/re/.local/share/waydroid/data/media/0/Android/data/com.mojang.minecraftpe/files/games/com.mojang/"

def report_progress(percent, status):
    """Envia o progresso formatado para o stdout em tempo real."""
    print(f"PROGRESS|{percent}|{status}")
    sys.stdout.flush()

def launch_game():
    """Inicia o container do Waydroid (se necessário) e abre o Minecraft."""
    status = subprocess.run("waydroid status | grep -q 'RUNNING'", shell=True)
    if status.returncode != 0:
        print("Iniciando sessão do Waydroid em background...")
        subprocess.Popen(["waydroid", "session", "start"])
        time.sleep(5)
    
    subprocess.run(["waydroid", "app", "launch", "com.mojang.minecraftpe"])

def install_game(apk_path=None):
    """Instala o arquivo APK local diretamente no ambiente Waydroid."""
    if not apk_path or apk_path.strip() == "":
        report_progress(100, "Erro: Nenhum arquivo APK foi fornecido.")
        return

    if not os.path.exists(apk_path):
        report_progress(100, "Erro: Arquivo APK não encontrado no caminho especificado.")
        return
    
    try:
        report_progress(20, "Verificando ambiente Waydroid...")
        status = subprocess.run("waydroid status | grep -q 'RUNNING'", shell=True)
        if status.returncode != 0:
            report_progress(40, "Ligando o container Waydroid...")
            subprocess.Popen(["waydroid", "session", "start"])
            time.sleep(4)
        
        report_progress(70, "Injetando APK local no container Waydroid...")
        result = subprocess.run(["waydroid", "app", "install", apk_path], capture_output=True, text=True)
        
        if result.returncode == 0:
            report_progress(100, "Minecraft instalado com sucesso!")
        else:
            erro_msg = result.stderr.strip() if result.stderr else "Erro desconhecido no container."
            report_progress(100, f"Erro na instalação: {erro_msg}")
            
    except Exception as e:
        report_progress(100, f"Falha crítica: {str(e)}")

def import_mod(file_path):
    """Injeta pacotes .mcpack, .mcaddon e .mcworld nas pastas do Minecraft."""
    if not os.path.exists(file_path):
        report_progress(100, "Erro: Arquivo do mod não encontrado.")
        return

    ext = os.path.splitext(file_path)[1].lower()
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    worlds_dir = os.path.join(MINECRAFT_DIR, "minecraftWorlds")
    behavior_dir = os.path.join(MINECRAFT_DIR, "behavior_packs")
    resource_dir = os.path.join(MINECRAFT_DIR, "resource_packs")
    
    # Assegura que a estrutura de diretórios alvo existe
    for folder in [worlds_dir, behavior_dir, resource_dir]:
        os.makedirs(folder, exist_ok=True)

    try:
        report_progress(15, f"Analisando integridade do pacote {ext}...")
        
        if ext == ".mcworld":
            target_dir = os.path.join(worlds_dir, base_name)
            os.makedirs(target_dir, exist_ok=True)
            report_progress(60, "Extraindo dados do mapa no cluster Waydroid...")
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(target_dir)
            report_progress(100, "Mundo importado com sucesso!")

        elif ext in [".mcpack", ".mcaddon"]:
            temp_extract = os.path.join("/tmp", f"mc_launcher_temp_{base_name}")
            if os.path.exists(temp_extract):
                shutil.rmtree(temp_extract)
            os.makedirs(temp_extract, exist_ok=True)
            
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_extract)
            
            has_behavior = False
            has_resource = False
            
            # Varredura inteligente de componentes internos do addon
            if "behavior" in file_path.lower() or os.path.exists(os.path.join(temp_extract, "entities")) or os.path.exists(os.path.join(temp_extract, "animation_controllers")):
                has_behavior = True
            if "resource" in file_path.lower() or os.path.exists(os.path.join(temp_extract, "textures")) or os.path.exists(os.path.join(temp_extract, "models")):
                has_resource = True
                
            if not has_behavior and not has_resource:
                has_resource = True  # Fallback padrão
                
            report_progress(70, "Injetando modificações estruturais nos dados do jogo...")
            
            if ext == ".mcaddon" or (has_behavior and has_resource):
                shutil.copytree(temp_extract, os.path.join(behavior_dir, f"{base_name}_B"), dirs_exist_ok=True)
                shutil.copytree(temp_extract, os.path.join(resource_dir, f"{base_name}_R"), dirs_exist_ok=True)
            elif has_behavior:
                shutil.copytree(temp_extract, os.path.join(behavior_dir, base_name), dirs_exist_ok=True)
            else:
                shutil.copytree(temp_extract, os.path.join(resource_dir, base_name), dirs_exist_ok=True)
                
            shutil.rmtree(temp_extract)
            report_progress(100, f"Pacote {ext} instalado com sucesso!")
            
    except Exception as e:
        report_progress(100, f"Falha na injeção: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "launch":
            launch_game()
        elif command == "install":
            apk_arg = sys.argv[2] if len(sys.argv) > 2 else ""
            install_game(apk_arg)
        elif command == "import-mod":
            file_arg = sys.argv[2] if len(sys.argv) > 2 else ""
            import_mod(file_arg)