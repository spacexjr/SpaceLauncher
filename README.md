# 🚀 SpaceLauncher

Launcher moderno para **Minecraft Bedrock Edition no Linux**, utilizando **Waydroid** como ambiente Android. O SpaceLauncher simplifica a instalação, inicialização e gerenciamento de mods para o Minecraft Bedrock, oferecendo uma interface moderna baseada em Electron.

---

## ✨ Recursos

* 🎮 Inicialização automática do Minecraft Bedrock
* 📦 Instalação de APKs diretamente no Waydroid
* 🌍 Importação de mundos, texturas e addons
* 🚀 Inicialização automática da sessão Waydroid
* 🌌 Interface espacial moderna e animada

---

## 📋 Requisitos de Software

### Sistema Operacional

* Linux x86_64
* Kernel com suporte a namespaces e binderfs
* Wayland ou X11

### Dependências

* Python 3.10+
* Electron 28+
* Waydroid
* Node.js 22+
* Minecraft Bedrock APK x86_64

---

# 💻 Requisitos de Hardware

## Requisitos Mínimos

| Componente    | Requisito                               |
| ------------- | --------------------------------------- |
| CPU           | Intel Core i3 4ª Geração ou AMD FX-6300 |
| RAM           | 8 GB                                    |
| GPU           | Intel HD 4600 / Vega 3 / GT 1030        |
| Armazenamento | 10 GB livres                            |


## Requisitos Recomendados

| Componente | Requisito                                |
| ---------- | ---------------------------------------- |
| CPU        | Intel Core i5 8ª Geração ou Ryzen 5 2600 |
| RAM        | 16 GB                                    |
| GPU        | GTX 1650 / RX 570 ou superior            |
| SSD        | Recomendado                              |

**Recomendação:** mínimo de 8 GB de RAM e idealmente 16 GB ou mais.

---

## 📦 Formatos Suportados

| Extensão   | Função                    |
| ---------- | ------------------------- |
| `.apk`     | Instalação do Minecraft   |
| `.mcworld` | Importação de mundos      |
| `.mcpack`  | Resource Packs            |
| `.mcaddon` | Addons                    |

---

## 🎮 Como Utilizar

### Instalar Minecraft

1. Abra a aba **Install**
2. Clique em **Localizar Arquivo APK**
3. Selecione o APK do Minecraft
4. Clique em **Iniciar Injeção**
5. Aguarde a conclusão

### Iniciar o Jogo

1. Vá para a aba **Launch**
2. Abra o jogo
3. O launcher iniciará automaticamente o Waydroid e abrirá o Minecraft

### Instalar Mods

1. Abra a aba **Mods**
2. Selecione um arquivo:

   * `.mcworld`
   * `.mcpack`
   * `.mcaddon`
3. Clique em **Instalar no Minecraft**
4. Abra o jogo

---

## 📂 Estrutura Utilizada

```text
minecraftWorlds/
resource_packs/
behavior_packs/
```

Os arquivos são instalados diretamente dentro do armazenamento Android do Waydroid:

```text
~/.local/share/waydroid/data/media/0/Android/data/com.mojang.minecraftpe/files/games/com.mojang/
```

---

## ⚠️ Observações

* O launcher não distribui APKs do Minecraft.
* É necessário possuir uma cópia legítima do jogo.
* O desempenho depende da aceleração gráfica do Waydroid.
* GPUs muito antigas podem apresentar limitações.
* O .apk tem que ser x86_64

---

## 🛠️ Tecnologias

* Electron
* Node.js
* Python
* HTML5
* CSS3
* JavaScript
* Waydroid

---

## 📜 Licença

Este projeto é distribuído sob a licença MIT.

---

# 🚀 SpaceLauncher

**Sua plataforma de lançamento para Minecraft Bedrock no Linux.**
