fn main() {
    #[cfg(windows)]
    {
        use std::io::Write;
        let mut res = winres::WindowsResource::new();
        // 版本资源跟随 APP_NAME，避免残留 RustDesk 特征
        let app_name = std::env::var("APP_NAME").unwrap_or_else(|_| "remote".to_owned());
        res.set_icon("../../res/icon.ico")
            .set_language(winapi::um::winnt::MAKELANGID(
                winapi::um::winnt::LANG_ENGLISH,
                winapi::um::winnt::SUBLANG_ENGLISH_US,
            ))
            .set("CompanyName", &app_name)
            .set("FileDescription", "Remote Desktop")
            .set("InternalName", &app_name)
            .set("OriginalFilename", &format!("{}.exe", app_name))
            .set("ProductName", &app_name)
            .set("LegalCopyright", "Copyright © 2025 All rights reserved.")
            .set_manifest_file("../../res/manifest.xml");
        match res.compile() {
            Err(e) => {
                write!(std::io::stderr(), "{}", e).unwrap();
                std::process::exit(1);
            }
            Ok(_) => {}
        }
    }
}
