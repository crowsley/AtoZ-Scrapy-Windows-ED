"""
AtoZ Scrapy Windows ED 0.0.1 - Windows Standalone Executable Build Script

Automates compiling the Windows Desktop Application into a standalone .exe
using PyInstaller.

Usage:
    python build_windows_exe.py
"""

import sys
import os
import subprocess


def build_exe():
    print("=========================================================")
    print(" Building AtoZ Scrapy Windows ED 0.0.1 Standalone .exe   ")
    print("=========================================================")

    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name=AtoZ-Scrapy-Windows-ED",
        "--add-data=scrapy;scrapy",
        "scrapy/gui/main_gui.py"
    ]

    print(f"Executing: {' '.join(cmd)}")
    subprocess.check_call(cmd)

    print("\n✅ Build complete! Executable generated in: dist/AtoZ-Scrapy-Windows-ED/AtoZ-Scrapy-Windows-ED.exe")


if __name__ == "__main__":
    build_exe()
