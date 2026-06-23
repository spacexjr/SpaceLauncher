const { app, BrowserWindow, ipcMain } = require('electron');
const { exec } = require('child_process');
const path = require('path');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 450,
        height: 600,
        resizable: false,
        autoHideMenuBar: true, // Remove a barra de menu feia de cima
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    mainWindow.loadFile('index.html');
}

// Escuta o evento do botão "JOGAR"
ipcMain.on('start-game', (event) => {
    // Chama o script Python que criamos
    exec('python3 bridge.py launch', (error, stdout, stderr) => {
        if (error) {
            console.error(`Erro: ${error}`);
        }
        // Avisa a interface que o processo terminou
        event.reply('game-started');
    });
});

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
});