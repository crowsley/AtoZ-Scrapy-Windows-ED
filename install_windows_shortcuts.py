"""
AtoZ Scrapy Windows ED 0.0.1 - Windows Start Menu & Desktop Shortcut Installer
"""

import os
import sys
import subprocess


def create_windows_shortcut():
    folder_path = r"C:\Users\saghi\Downloads\AtoZ Scrapy Windows 11 ED"
    vbs_path = os.path.join(folder_path, "Start-AtoZ-Scrapy.vbs")

    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    start_menu = os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs")

    shortcut_desktop = os.path.join(desktop, "AtoZ Scrapy Windows 11 ED.lnk")
    shortcut_start = os.path.join(start_menu, "AtoZ Scrapy Windows 11 ED.lnk")

    cmd = (
        f"$s = (New-Object -ComObject WScript.Shell).CreateShortcut('{shortcut_desktop}'); "
        f"$s.TargetPath = 'wscript.exe'; "
        f"$s.Arguments = '\"{vbs_path}\"'; "
        f"$s.WorkingDirectory = '{folder_path}'; "
        f"$s.Save(); "
        f"$s2 = (New-Object -ComObject WScript.Shell).CreateShortcut('{shortcut_start}'); "
        f"$s2.TargetPath = 'wscript.exe'; "
        f"$s2.Arguments = '\"{vbs_path}\"'; "
        f"$s2.WorkingDirectory = '{folder_path}'; "
        f"$s2.Save();"
    )

    try:
        res = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
        print("✅ Created shortcuts for AtoZ Scrapy Windows 11 ED on Desktop & Start Menu.")
    except Exception as e:
        print(f"Shortcut creation error: {e}")


if __name__ == "__main__":
    create_windows_shortcut()
