import sys
import os
import subprocess
import urllib.request
import time

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
        # Aguarda o container subir completamente antes de lançar o app
        time.sleep(5)
    
    subprocess.run(["waydroid", "app", "launch", "com.mojang.minecraftpe"])

def install_game(apk_url=None):
    """Instala o APK, aceitando tanto um link HTTP/HTTPS quanto um caminho local."""
    if not apk_url or apk_url.strip() == "":
        report_progress(100, "Erro: Nenhum arquivo ou URL fornecida.")
        return

    # Detecta se o arquivo já está baixado no computador (caminho absoluto)
    if apk_url.startswith("/") or os.path.exists(apk_url):
        target_apk = apk_url
        is_local = True
    else:
        target_apk = "/tmp/minecraft_bedrock.apk"
        is_local = False
    
    try:
        report_progress(10, "Verificando ambiente Waydroid...")
        # Garante que o serviço do Waydroid esteja ativo antes de instalar
        status = subprocess.run("waydroid status | grep -q 'RUNNING'", shell=True)
        if status.returncode != 0:
            report_progress(20, "Ligando o container Waydroid...")
            subprocess.Popen(["waydroid", "session", "start"])
            time.sleep(4)
        
        # Gerenciamento de Origem: Web vs Computador Local
        if not is_local:
            report_progress(30, "Fazendo download do instalador APK...")
            def download_hook(count, block_size, total_size):
                if total_size > 0:
                    progress = int(count * block_size * 100 / total_size)
                    ui_progress = 30 + int(progress * 0.4) # Normaliza entre 30% e 70%
                    if ui_progress <= 70:
                        report_progress(ui_progress, f"Baixando APK: {progress}%")
            urllib.request.urlretrieve(apk_url, target_apk, reporthook=download_hook)
        else:
            report_progress(50, "Arquivo local detectado. Preparando instalação...")
        
        # Injeção do pacote para o Waydroid
        report_progress(80, "Injetando APK no container Waydroid...")
        result = subprocess.run(["waydroid", "app", "install", target_apk], capture_output=True, text=True)
        
        if result.returncode == 0:
            report_progress(100, "Minecraft instalado com sucesso!")
        else:
            # Captura a mensagem real de erro do próprio binário do Waydroid
            erro_msg = result.stderr.strip() if result.stderr else "Erro desconhecido no container."
            report_progress(100, f"Erro na instalação: {erro_msg}")
            
        # Limpa o arquivo temporário apenas se ele tiver sido baixado da Web
        if not is_local and os.path.exists(target_apk):
            os.remove(target_apk)
            
    except Exception as e:
        report_progress(100, f"Falha crítica: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "launch":
            launch_game()
        elif command == "install":
            # Captura o caminho do arquivo passado pelo Electron
            url_arg = sys.argv[2] if len(sys.argv) > 2 else ""
            install_game(url_arg)