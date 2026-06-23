const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const { exec } = require('child_process');
const path = require('path');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1000,
        height: 600,
        resizable: true,
        frame: false, // Ativa o modo sem bordas (custom top-bar)
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    mainWindow.loadFile('index.html');
}

// Gerenciamento dos botões nativos da janela customizada
ipcMain.on('window-minimize', () => mainWindow.minimize());
ipcMain.on('window-close', () => mainWindow.close());

// Escuta o pedido da interface para abrir o seletor de arquivos local (APK)
ipcMain.handle('open-file-dialog', async () => {
    const result = await dialog.showOpenDialog(mainWindow, {
        title: 'Selecione o APK do Minecraft Bedrock',
        properties: ['openFile'],
        filters: [
            { name: 'Arquivos APK', extensions: ['apk'] }
        ]
    });

    if (!result.canceled && result.filePaths.length > 0) {
        return result.filePaths[0]; // Retorna o caminho absoluto do arquivo
    }
    return null;
});

// Ação de Lançar o Jogo
ipcMain.on('start-game', (event) => {
    exec('python3 bridge.py launch', (error) => {
        if (error) console.error(`Erro ao lançar: ${error}`);
        event.reply('game-started');
    });
});

// Ação de Instalar o Jogo via arquivo APK local
ipcMain.on('install-game', (event, filePath) => {
    // Passa o caminho do arquivo entre aspas para evitar quebras por espaços no nome
    const pythonProcess = exec(`python3 bridge.py install "${filePath}"`);

    pythonProcess.stdout.on('data', (data) => {
        const output = data.toString().trim();
        if (output.startsWith("PROGRESS|")) {
            const parts = output.split("|");
            const percent = parts[1];
            const status = parts[2];
            
            // Retorna o progresso em tempo real para a barra de carregamento no HTML
            mainWindow.webContents.send('install-progress', { 
                percent: parseInt(percent), 
                status: status 
            });
        }
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Erro no script Python: ${data}`);
    });
});

app.whenReady().then(createWindow);

app.on('window-all-closed', () => { 
    if (process.platform !== 'darwin') app.quit(); 
});