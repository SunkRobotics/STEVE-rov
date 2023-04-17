#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

// use tauri::Manager;
// use tauri::App;

fn main() {
    tauri::Builder::default()
        .setup(|_| {
            tauri::async_runtime::spawn(async move { steve_client::run() });
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
