use std::fs;
use std::path::PathBuf;
use tauri::command;

const COH_DATA: &str = "/Applications/coh/data";

fn downloads_dir(app: &tauri::AppHandle) -> PathBuf {
    app.path().app_data_dir()
        .unwrap_or_else(|_| PathBuf::from("."))
        .join("downloads")
}

// #[command] exposes this function to the web frontend via window.__TAURI__.invoke()
// Equivalent to Electron's ipcMain.handle('get-installed', ...)
#[command]
fn get_installed(app: tauri::AppHandle) -> Vec<String> {
    let dir = if fs::metadata(COH_DATA).is_ok() {
        PathBuf::from(COH_DATA)
    } else {
        downloads_dir(&app)
    };

    fs::read_dir(&dir)
        .into_iter()
        .flatten()
        .filter_map(|e| e.ok())
        .filter(|e| e.path().extension().and_then(|x| x.to_str()) == Some("pigg"))
        .filter_map(|e| {
            e.path().file_stem()
                .and_then(|s| s.to_str())
                .map(String::from)
        })
        .collect()
}

#[derive(serde::Serialize)]
struct InstallResult {
    ok: bool,
    path: Option<String>,
    error: Option<String>,
}

// Downloads a .pigg mod file — reqwest replaces Node's https.get()
#[command]
async fn install_mod(app: tauri::AppHandle, url: String, id: u64) -> InstallResult {
    let fname = url.split("file=").last()
        .and_then(|s| s.split('/').last())
        .unwrap_or("unknown.pigg")
        .to_string();

    let dest = if fs::metadata(COH_DATA).is_ok() {
        PathBuf::from(COH_DATA).join(&fname)
    } else {
        let dl = downloads_dir(&app);
        let _ = fs::create_dir_all(&dl);
        dl.join(&fname)
    };

    match reqwest::get(&url).await {
        Ok(resp) if resp.status().is_success() => {
            match resp.bytes().await {
                Ok(bytes) => {
                    if let Err(e) = fs::write(&dest, &bytes) {
                        return InstallResult { ok: false, path: None, error: Some(e.to_string()) }
                    }
                    InstallResult { ok: true, path: Some(dest.to_string_lossy().into()), error: None }
                }
                Err(e) => InstallResult { ok: false, path: None, error: Some(e.to_string()) },
            }
        }
        Ok(resp) => InstallResult { ok: false, path: None, error: Some(format!("HTTP {}", resp.status())) },
        Err(e)   => InstallResult { ok: false, path: None, error: Some(e.to_string()) },
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![get_installed, install_mod])
        .run(tauri::generate_context!())
        .expect("error running tauri app");
}
