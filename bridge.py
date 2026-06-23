import sys
import subprocess
import time

def launch_game():
    # Verifica se o Waydroid está rodando
    status = subprocess.run("waydroid status | grep -q 'RUNNING'", shell=True)
    
    if status.returncode != 0:
        # Se não estiver rodando, inicia a sessão
        subprocess.Popen(["waydroid", "session", "start"])
        time.sleep(4) # Aguarda o container subir
        
    # Lança o Minecraft
    subprocess.run(["waydroid", "app", "launch", "com.mojang.minecraftpe"])

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "launch":
        launch_game()
        print("SUCCESS")