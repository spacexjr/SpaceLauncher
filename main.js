const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const { exec } = require('child_process');
const path = require('path');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1000,
        height: 600,
        resizable: true,
        frame: false, 
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    mainWindow.loadFile('index.html');
}

ipcMain.on('window-minimize', () => mainWindow.minimize());
ipcMain.on('window-close', () => mainWindow.close());

// Seletor de Arquivos para o APK
ipcMain.handle('open-file-dialog', async () => {
    const result = await dialog.showOpenDialog(mainWindow, {
        title: 'Selecione o APK do Minecraft Bedrock',
        properties: ['openFile'],
        filters: [
            { name: 'Arquivos APK', extensions: ['apk'] }
        ]
    });

    if (!result.canceled && result.filePaths.length > 0) {
        return result.filePaths[0]; 
    }
    return null;
});

// Seletor de Arquivos para Complementos/Mods
ipcMain.handle('open-mod-dialog', async () => {
    const result = await dialog.showOpenDialog(mainWindow, {
        title: 'Selecione complementos do Minecraft (.mcpack, .mcaddon, .mcworld)',
        properties: ['openFile'],
        filters: [
            { name: 'Minecraft Addons & Worlds', extensions: ['mcpack', 'mcaddon', 'mcworld'] }
        ]
    });

    if (!result.canceled && result.filePaths.length > 0) {
        return result.filePaths[0];
    }
    return null;
});

// Lançamento do jogo
ipcMain.on('start-game', (event) => {
    exec('python3 bridge.py launch', (error) => {
        if (error) console.error(`Erro ao lançar: ${error}`);
        event.reply('game-started');
    });
});

// Instalação do APK
ipcMain.on('install-game', (event, filePath) => {
    const pythonProcess = exec(`python3 bridge.py install "${filePath}"`);

    pythonProcess.stdout.on('data', (data) => {
        const output = data.toString().trim();
        if (output.startsWith("PROGRESS|")) {
            const parts = output.split("|");
            const percent = parts[1];
            const status = parts[2];
            
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

// Importação de Modificações e Mapas
ipcMain.on('import-mod', (event, filePath) => {
    const pythonProcess = exec(`pkexec python3 "${path.join(__dirname, 'bridge.py')}" import-mod "${filePath}"`);

    pythonProcess.stdout.on('data', (data) => {
        const output = data.toString().trim();
        if (output.startsWith("PROGRESS|")) {
            const parts = output.split("|");
            const percent = parts[1];
            const status = parts[2];
            
            mainWindow.webContents.send('mod-progress', { 
                percent: parseInt(percent), 
                status: status 
            });
        }
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Erro no script Python (Mods): ${data}`);
    });
});

app.whenReady().then(createWindow);

app.on('window-all-closed', () => { 
    if (process.platform !== 'darwin') app.quit(); 
});