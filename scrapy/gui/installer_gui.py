"""
AtoZ Scrapy Windows ED 0.0.1 - Graphical Windows Setup Installer Wizard

Displays a standard Windows software setup wizard that installs AtoZ Scrapy Windows ED
to Program Files / AppData, creates Start Menu & Desktop shortcuts, and launches the app.
"""

import sys
import os
import shutil
import zipfile
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import subprocess


class AtoZInstallerWizard:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("AtoZ Scrapy Windows 11 ED - Setup Wizard")
        self.root.geometry("600x420")
        self.root.resizable(False, False)

        # Style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        bg_color = "#f0f0f0"
        self.root.configure(bg=bg_color)

        default_install_dir = os.path.join(os.environ.get("LOCALAPPDATA", r"C:\Users\Public"), "AtoZ-Scrapy-Windows-11-ED")
        self.install_dir_var = tk.StringVar(value=default_install_dir)

        self._build_welcome_page()

    def _build_welcome_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Banner Left
        banner = tk.Frame(self.root, bg="#0078d4", width=180, height=420)
        banner.pack(side="left", fill="y")

        lbl_b = tk.Label(banner, text="🚀\n\nAtoZ Scrapy\nWindows 11 ED\nSetup", bg="#0078d4", fg="white", font=("Segoe UI", 12, "bold"))
        lbl_b.pack(pady=40, padx=15)

        # Main Content Right
        main_frame = tk.Frame(self.root, bg="#ffffff", padding=20)
        main_frame.pack(side="right", fill="both", expand=True)

        title = tk.Label(main_frame, text="Welcome to the Setup Wizard", font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#0078d4")
        title.pack(anchor="w", pady=(10, 5))

        desc = tk.Label(
            main_frame,
            text="This wizard will install AtoZ Scrapy Windows 11 ED (v0.0.1) on your computer.\n\n"
                 "Click Next to continue or Cancel to exit Setup.",
            justify="left",
            bg="#ffffff",
            font=("Segoe UI", 10)
        )
        desc.pack(anchor="w", pady=10)

        # Directory selection
        tk.Label(main_frame, text="Destination Folder:", font=("Segoe UI", 9, "bold"), bg="#ffffff").pack(anchor="w", pady=(15, 2))
        dir_frame = tk.Frame(main_frame, bg="#ffffff")
        dir_frame.pack(fill="x", pady=5)

        entry_dir = ttk.Entry(dir_frame, textvariable=self.install_dir_var, width=35)
        entry_dir.pack(side="left", fill="x", expand=True)

        btn_browse = ttk.Button(dir_frame, text="Browse...", command=self._browse_dir)
        btn_browse.pack(side="left", padx=5)

        # Buttons bottom
        btn_frame = tk.Frame(main_frame, bg="#ffffff")
        btn_frame.pack(side="bottom", fill="x", pady=10)

        ttk.Button(btn_frame, text="Cancel", command=self.root.destroy).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Install ▶", command=self._start_installation).pack(side="right", padx=5)

    def _browse_dir(self):
        chosen = filedialog.askdirectory(initialdir=self.install_dir_var.get())
        if chosen:
            self.install_dir_var.set(chosen)

    def _start_installation(self):
        target_dir = self.install_dir_var.get()
        if not target_dir:
            messagebox.showwarning("Setup Warning", "Please select a valid installation folder.")
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        banner = tk.Frame(self.root, bg="#0078d4", width=180, height=420)
        banner.pack(side="left", fill="y")
        tk.Label(banner, text="⚙️\n\nInstalling...", bg="#0078d4", fg="white", font=("Segoe UI", 12, "bold")).pack(pady=40, padx=15)

        main_frame = tk.Frame(self.root, bg="#ffffff", padding=20)
        main_frame.pack(side="right", fill="both", expand=True)

        tk.Label(main_frame, text="Installing AtoZ Scrapy Windows 11 ED", font=("Segoe UI", 13, "bold"), bg="#ffffff", fg="#0078d4").pack(anchor="w", pady=(10, 5))

        self.lbl_status = tk.Label(main_frame, text="Copying application files...", bg="#ffffff", font=("Segoe UI", 9))
        self.lbl_status.pack(anchor="w", pady=10)

        self.progress = ttk.Progressbar(main_frame, orient="horizontal", mode="determinate", length=320)
        self.progress.pack(fill="x", pady=10)

        threading.Thread(target=self._run_install_task, args=(target_dir,), daemon=True).start()

    def _run_install_task(self, target_dir: str):
        try:
            os.makedirs(target_dir, exist_ok=True)
            self.progress['value'] = 30
            self.lbl_status.config(text="Extracting binaries & dependencies...")

            source_exe = os.path.join(os.path.expanduser("~"), "Downloads", "AtoZ-Scrapy-Windows-11-ED.exe")
            dest_exe = os.path.join(target_dir, "AtoZ-Scrapy-Windows-11-ED.exe")


            if os.path.exists(source_exe):
                shutil.copy2(source_exe, dest_exe)

            self.progress['value'] = 70
            self.lbl_status.config(text="Creating Start Menu & Desktop shortcuts...")

            # Shortcuts
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            onedrive_desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
            start_menu = os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs")

            shortcut_desktop = os.path.join(desktop, "AtoZ Scrapy Windows 11 ED.lnk")
            shortcut_onedrive = os.path.join(onedrive_desktop, "AtoZ Scrapy Windows 11 ED.lnk")
            shortcut_start = os.path.join(start_menu, "AtoZ Scrapy Windows 11 ED.lnk")

            ps_cmd = (
                f"$s = (New-Object -ComObject WScript.Shell).CreateShortcut('{shortcut_desktop}'); "
                f"$s.TargetPath = '{dest_exe}'; $s.WorkingDirectory = '{target_dir}'; $s.Save(); "
                f"if (Test-Path '{onedrive_desktop}') {{ "
                f"  $s1 = (New-Object -ComObject WScript.Shell).CreateShortcut('{shortcut_onedrive}'); "
                f"  $s1.TargetPath = '{dest_exe}'; $s1.WorkingDirectory = '{target_dir}'; $s1.Save(); "
                f"}} "
                f"$s2 = (New-Object -ComObject WScript.Shell).CreateShortcut('{shortcut_start}'); "
                f"$s2.TargetPath = '{dest_exe}'; $s2.WorkingDirectory = '{target_dir}'; $s2.Save();"
            )
            subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True)

            self.progress['value'] = 100
            self.root.after(0, lambda: self._build_finish_page(dest_exe))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Setup Error", f"Installation failed: {str(e)}"))

    def _build_finish_page(self, installed_exe_path: str):
        for widget in self.root.winfo_children():
            widget.destroy()

        banner = tk.Frame(self.root, bg="#28a745", width=180, height=420)
        banner.pack(side="left", fill="y")
        tk.Label(banner, text="✅\n\nInstallation\nComplete!", bg="#28a745", fg="white", font=("Segoe UI", 12, "bold")).pack(pady=40, padx=15)

        main_frame = tk.Frame(self.root, bg="#ffffff", padding=20)
        main_frame.pack(side="right", fill="both", expand=True)

        tk.Label(main_frame, text="Completing the Setup Wizard", font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#28a745").pack(anchor="w", pady=(10, 5))

        tk.Label(
            main_frame,
            text="AtoZ Scrapy Windows 11 ED has been installed on your computer.\n\n"
                 "Shortcuts have been added to your Desktop and Start Menu.\n\n"
                 "Click Finish to exit Setup.",
            justify="left",
            bg="#ffffff",
            font=("Segoe UI", 10)
        ) .pack(anchor="w", pady=10)

        self.launch_var = tk.BooleanVar(value=True)
        chk_launch = tk.Checkbutton(
            main_frame,
            text="Launch AtoZ Scrapy Windows 11 ED now",
            variable=self.launch_var,
            bg="#ffffff",
            font=("Segoe UI", 10, "bold")
        )
        chk_launch.pack(anchor="w", pady=15)

        btn_frame = tk.Frame(main_frame, bg="#ffffff")
        btn_frame.pack(side="bottom", fill="x", pady=10)

        def finish():
            if self.launch_var.get() and os.path.exists(installed_exe_path):
                subprocess.Popen([installed_exe_path])
            self.root.destroy()

        ttk.Button(btn_frame, text="Finish ✔", command=finish).pack(side="right", padx=5)


def main():
    root = tk.Tk()
    app = AtoZInstallerWizard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
