const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const fs   = require('fs');
const https = require('https');
const http  = require('http');

const COH_DATA  = '/Applications/coh/data';
const DOWNLOADS = path.join(__dirname, 'downloads');

function createWindow() {
  const win = new BrowserWindow({
    width: 1400,
    height: 900,
    title: 'CoX Mod Archive',
    backgroundColor: '#05050f',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });
  win.loadFile('index.html');
}

// Return list of installed mod filestems from CoH data dir (or local downloads/)
ipcMain.handle('get-installed', () => {
  const target = fs.existsSync(COH_DATA) ? COH_DATA : DOWNLOADS;
  if (!fs.existsSync(target)) return [];
  return fs.readdirSync(target)
    .filter(f => f.endsWith('.pigg'))
    .map(f => path.basename(f, '.pigg'));
});

// Download a mod and place it in CoH data dir or local downloads/
ipcMain.handle('install-mod', (_event, { url, id }) => {
  return new Promise(resolve => {
    const fname  = (url.split('file=').pop() || '').split('/').pop() || `mod-${id}.pigg`;
    const dest   = fs.existsSync(COH_DATA)
      ? path.join(COH_DATA, fname)
      : path.join(DOWNLOADS, fname);

    fs.mkdirSync(path.dirname(dest), { recursive: true });

    const file   = fs.createWriteStream(dest);
    const getter = url.startsWith('https') ? https : http;

    getter.get(url, res => {
      if (res.statusCode !== 200) {
        resolve({ ok: false, error: `HTTP ${res.statusCode}` });
        return;
      }
      res.pipe(file);
      file.on('finish', () => file.close(() => resolve({ ok: true, path: dest, id })));
    }).on('error', err => {
      fs.unlink(dest, () => {});
      resolve({ ok: false, error: err.message });
    });
  });
});

app.whenReady().then(createWindow);
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
app.on('activate', () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(); });
