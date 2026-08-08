"""
AtoZ Scrapy Windows ED 0.0.1 - Windows Start Menu & Desktop Shortcut Installer
"""

import os
import sys
import subprocess


def create_windows_shortcut():
    print("Installing AtoZ Scrapy Windows ED Start Menu & Desktop Shortcuts...")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    vbs_path = os.path.join(current_dir, "Start-AtoZ-Scrapy.vbs")

    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    start_menu = os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs")

    shortcut_desktop = os.path.join(desktop, "AtoZ Scrapy Windows ED.lnk")
    shortcut_start = os.path.join(start_menu, "AtoZ Scrapy Windows ED.lnk")

    cmd = (
        f"$s = (New-Object -ComObject WScript.Shell).CreateShortcut('{shortcut_desktop}'); "
        f"$s.TargetPath = 'wscript.exe'; "
        f"$s.Arguments = '\"{vbs_path}\"'; "
        f"$s.WorkingDirectory = '{current_dir}'; "
        f"$s.Save(); "
        f"$s2 = (New-Object -ComObject WScript.Shell).CreateShortcut('{shortcut_start}'); "
        f"$s2.TargetPath = 'wscript.exe'; "
        f"$s2.Arguments = '\"{vbs_path}\"'; "
        f"$s2.WorkingDirectory = '{current_dir}'; "
        f"$s2.Save();"
    )

    try:
        res = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
        if res.returncode == 0:
            print("✅ Successfully installed AtoZ Scrapy Windows ED in Windows Start Menu and Desktop!")
        else:
            print(f"Error creating shortcut: {res.stderr}")
    except Exception as e:
        print(f"Failed to create shortcut: {e}")


if __name__ == "__main__":
    create_windows_shortcut()
