# 🚀 AtoZ Scrapy Windows ED 0.0.1

[![Release](https://img.shields.io/badge/version-0.0.1-blue.svg)](https://github.com/)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%20%7C%2011-0078D6.svg)](https://microsoft.com/windows)
[![License](https://img.shields.io/badge/license-BSD--3--Clause-green.svg)](LICENSE)

**AtoZ Scrapy Windows ED 0.0.1** (Enterprise Edition) is an enhanced, high-performance web crawling & web scraping framework specifically tailored as a native Windows desktop application. Built on top of Scrapy, it combines high-concurrency multi-worker crawling, headless browser rendering via Playwright, live item data streaming, and an integrated **GitHub Auto-Update System**.

---

## 🌟 Key Features

### 🖥️ Native Windows Desktop GUI
- **Spider Launcher**: Select, configure, and execute spiders visually without touching command prompt.
- **Live Scraped Data Table**: View scraped items in real-time as spiders parse websites.
- **Export Controls**: One-click data exports to CSV and JSON formats.

### ⚡ Windows Concurrency Engine
- **Windows IOCP Event Loop**: Harnesses Windows Proactor I/O (`WindowsProactorEventLoopPolicy`) for fast I/O throughput.
- **Multi-Process Workers**: Distributes spider requests across multiple CPU cores on your laptop.

### 🎭 Playwright & Anti-Bot Bypass
- **Dynamic JavaScript Support**: Integrated Playwright downloader middleware for rendering dynamic single-page applications (React, Vue, Angular).
- **Proxy Rotation**: Built-in HTTP/HTTPS/SOCKS proxy manager for rotating IP addresses.

### 🔄 GitHub Auto-Updater
- **Direct GitHub Sync**: Connects to your GitHub repository API (`releases/latest`) to check for updates.
- **One-Click In-App Upgrade**: Download and apply updates directly from the GUI tab when new commits/releases are pushed to GitHub.

---

## 🚀 Quick Start & Installation

### Prerequisites
- **Windows 10 or 11**
- **Python 3.9+**

### 1. Installation
Clone your repository or download the source code:

```powershell
git clone https://github.com/YOUR_USERNAME/AtoZ-Scrapy-Windows-ED.git
cd AtoZ-Scrapy-Windows-ED
pip install -e .
```

### 2. Launch the Desktop Application
Run the desktop GUI app using python:

```powershell
python -m scrapy.gui.main_gui
```

---

## 🔄 How GitHub Auto-Updating Works

1. Open the **`🔄 GitHub Updater`** tab in the desktop application.
2. Enter your GitHub repository path (e.g., `your-username/AtoZ-Scrapy-Windows-ED`).
3. Click **`Check GitHub for Updates`**.
4. If a new release or update tag is detected on GitHub, click **`Download & Install`** to sync your local Windows installation with GitHub automatically!

---

## 🛠️ Architecture & Project Structure

```
AtoZ-Scrapy-Windows-ED/
├── scrapy/
│   ├── gui/
│   │   ├── main_gui.py       # Desktop App Window & Controls
│   │   ├── updater.py        # GitHub Auto-Update Mechanism
│   │   └── version.py        # Version string (0.0.1) & Metadata
│   ├── core/
│   │   └── windows_engine.py # Windows IOCP Concurrency Engine
│   └── downloadermiddlewares/
│       └── playwright_middleware.py # Playwright Browser Automation
├── README.md                 # Project Documentation
└── pyproject.toml            # Project Dependencies & Configuration
```

---

## 📄 License
This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.
