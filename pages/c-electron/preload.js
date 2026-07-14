const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  getInstalled: ()          => ipcRenderer.invoke('get-installed'),
  installMod:  (url, id)   => ipcRenderer.invoke('install-mod', { url, id }),
});
