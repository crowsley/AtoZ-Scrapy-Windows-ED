"""
AtoZ Scrapy Windows ED 0.0.1 - Desktop & Start Menu Shortcut Installer for Standalone .exe
"""

import os
import subprocess


def create_exe_shortcut():
    exe_path = r"C:\Users\saghi\Downloads\AtoZ-Scrapy-Windows-11-ED.exe"
    folder_path = r"C:\Users\saghi\Downloads"

    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    onedrive_desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
    start_menu = os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs")

    shortcut_desktop = os.path.join(desktop, "AtoZ Scrapy Windows 11 ED.lnk")
    shortcut_onedrive = os.path.join(onedrive_desktop, "AtoZ Scrapy Windows 11 ED.lnk")
    shortcut_start = os.path.join(start_menu, "AtoZ Scrapy Windows 11 ED.lnk")

    cmd = (
        f"$s = (New-Object -ComObject WScript.Shell).CreateShortcut('{shortcut_desktop}'); "
        f"$s.TargetPath = '{exe_path}'; "
        f"$s.WorkingDirectory = '{folder_path}'; "
        f"$s.Save(); "
        f"if (Test-Path '{onedrive_desktop}') {{ "
        f"  $s1 = (New-Object -ComObject WScript.Shell).CreateShortcut('{shortcut_onedrive}'); "
        f"  $s1.TargetPath = '{exe_path}'; "
        f"  $s1.WorkingDirectory = '{folder_path}'; "
        f"  $s1.Save(); "
        f"}} "
        f"$s2 = (New-Object -ComObject WScript.Shell).CreateShortcut('{shortcut_start}'); "
        f"$s2.TargetPath = '{exe_path}'; "
        f"$s2.WorkingDirectory = '{folder_path}'; "
        f"$s2.Save();"
    )

    try:
        res = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
        print("[SUCCESS] Standalone .exe shortcuts created on Windows Desktop & Start Menu.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    create_exe_shortcut()
