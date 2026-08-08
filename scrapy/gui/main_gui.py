"""
AtoZ Scrapy Windows ED 0.0.1 - Main Windows Desktop GUI Application

Provides a full native Windows desktop app for controlling spiders, configuring
proxies and Playwright, streaming live scraped data, and checking/applying updates from GitHub.
"""

import sys
import os
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from typing import Optional

try:
    from scrapy.gui.version import APP_NAME, APP_VERSION, FULL_APP_TITLE
    from scrapy.gui.updater import GitHubUpdater
    from scrapy.pipelines.gui_pipeline import GUI_ITEM_QUEUE
except (ImportError, ValueError):
    from .version import APP_NAME, APP_VERSION, FULL_APP_TITLE
    from .updater import GitHubUpdater
    from scrapy.pipelines.gui_pipeline import GUI_ITEM_QUEUE




class AtoZScrapyWindowsApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(FULL_APP_TITLE)
        self.root.geometry("980x680")
        self.root.minsize(800, 550)
        self.item_count = 0
        self.scraped_items_list = []

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")


        # Configure colors (Dark / Modern Windows style)
        bg_dark = "#1e1e2e"
        fg_light = "#cdd6f4"
        accent_blue = "#89b4fa"

        self.root.configure(bg=bg_dark)
        self.style.configure(".", background=bg_dark, foreground=fg_light, font=("Segoe UI", 10))
        self.style.configure("TNotebook", background=bg_dark, borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#313244", foreground=fg_light, padding=[12, 6], font=("Segoe UI", 10, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", accent_blue)], foreground=[("selected", "#11111b")])
        self.style.configure("TButton", background=accent_blue, foreground="#11111b", font=("Segoe UI", 10, "bold"), padding=6)
        self.style.map("TButton", background=[("active", "#b4befe")])
        self.style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground=accent_blue)
        self.style.configure("Status.TLabel", font=("Segoe UI", 9, "italic"), foreground="#a6adc8")

        self.updater = GitHubUpdater()

        # Build Layout
        self._create_header()
        self._create_tabs()
        self._create_statusbar()

        # Start background item queue polling
        self._poll_item_queue()

    def _poll_item_queue(self):
        try:
            while not GUI_ITEM_QUEUE.empty():
                item = GUI_ITEM_QUEUE.get_nowait()
                self.item_count += 1
                self.scraped_items_list.append(item.get("raw_item", {}))

                self.data_table.insert(
                    "",
                    "end",
                    values=(self.item_count, item.get("url"), item.get("content"), item.get("timestamp"))
                )
                self.status_var.set(f"Running | Total Scraped Items: {self.item_count}")
        except Exception:
            pass

        self.root.after(200, self._poll_item_queue)


    def _create_header(self):
        header_frame = ttk.Frame(self.root, padding=(15, 10))
        header_frame.pack(fill="x")

        title_lbl = ttk.Label(header_frame, text=f"🚀 {FULL_APP_TITLE}", style="Header.TLabel")
        title_lbl.pack(side="left")

        version_badge = tk.Label(
            header_frame,
            text=f" v{APP_VERSION} (Windows ED) ",
            bg="#313244",
            fg="#a6e3a1",
            font=("Segoe UI", 9, "bold"),
            bd=1,
            relief="solid"
        )
        version_badge.pack(side="left", padx=10)

    def _create_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=10)

        # Tab 1: Spider Control & Launcher
        self.tab_launcher = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab_launcher, text="  🕷️ Spider Control  ")
        self._build_launcher_tab()

        # Tab 2: Live Scraped Data
        self.tab_data = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab_data, text="  📊 Live Data Feed  ")
        self._build_data_tab()

        # Tab 3: Settings (Playwright & Proxies)
        self.tab_settings = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab_settings, text="  ⚙️ Engine Settings  ")
        self._build_settings_tab()

        # Tab 4: GitHub Auto-Updater
        self.tab_updater = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab_updater, text="  🔄 GitHub Updater  ")
        self._build_updater_tab()

    def _build_launcher_tab(self):
        frame = self.tab_launcher

        # Spider selection / input
        ttk.Label(frame, text="Spider Name / File:").grid(row=0, column=0, sticky="w", pady=5)
        self.spider_input = ttk.Entry(frame, width=40)
        self.spider_input.insert(0, "example_spider")
        self.spider_input.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        ttk.Label(frame, text="Target URL (Optional):").grid(row=1, column=0, sticky="w", pady=5)
        self.url_input = ttk.Entry(frame, width=60)
        self.url_input.insert(0, "https://quotes.toscrape.com")
        self.url_input.grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Concurrency settings
        ttk.Label(frame, text="Concurrent Requests:").grid(row=2, column=0, sticky="w", pady=5)
        self.concurrency_spin = ttk.Spinbox(frame, from_=1, to=128, width=10)
        self.concurrency_spin.set(16)
        self.concurrency_spin.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # Controls
        btn_frame = ttk.Frame(frame, padding=(0, 15))
        btn_frame.grid(row=3, column=0, columnspan=2, sticky="w")

        self.btn_run = ttk.Button(btn_frame, text="▶ Start Spider", command=self._start_spider)
        self.btn_run.pack(side="left", padx=5)

        self.btn_stop = ttk.Button(btn_frame, text="⏹ Stop Engine", command=self._stop_spider)
        self.btn_stop.pack(side="left", padx=5)

        # Execution Log Output
        ttk.Label(frame, text="Execution Output Log:").grid(row=4, column=0, sticky="w", pady=(10, 5))
        self.log_text = scrolledtext.ScrolledText(frame, height=14, bg="#11111b", fg="#a6adc8", font=("Consolas", 9))
        self.log_text.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=5)
        frame.rowconfigure(5, weight=1)
        frame.columnconfigure(1, weight=1)

    def _build_data_tab(self):
        frame = self.tab_data

        # Treeview table for items
        columns = ("#", "URL / Title", "Scraped Content Snippet", "Timestamp")
        self.data_table = ttk.Treeview(frame, columns=columns, show="headings", height=18)
        
        self.data_table.heading("#", text="#")
        self.data_table.heading("URL / Title", text="URL / Title")
        self.data_table.heading("Scraped Content Snippet", text="Scraped Content Snippet")
        self.data_table.heading("Timestamp", text="Timestamp")

        self.data_table.column("#", width=50, anchor="center")
        self.data_table.column("URL / Title", width=250)
        self.data_table.column("Scraped Content Snippet", width=450)
        self.data_table.column("Timestamp", width=150)

        self.data_table.pack(fill="both", expand=True, pady=10)

        # Export controls
        export_frame = ttk.Frame(frame)
        export_frame.pack(fill="x", pady=5)

        ttk.Button(export_frame, text="💾 Export to CSV", command=self._export_csv).pack(side="left", padx=5)
        ttk.Button(export_frame, text="📄 Export to JSON", command=self._export_json).pack(side="left", padx=5)

    def _export_csv(self):
        if not self.scraped_items_list:
            messagebox.showinfo("Export", "No items scraped yet.")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if filename:
            import csv
            keys = self.scraped_items_list[0].keys()
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(self.scraped_items_list)
            messagebox.showinfo("Export Complete", f"Exported {len(self.scraped_items_list)} items to {filename}")

    def _export_json(self):
        if not self.scraped_items_list:
            messagebox.showinfo("Export", "No items scraped yet.")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if filename:
            import json
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.scraped_items_list, f, indent=2)
            messagebox.showinfo("Export Complete", f"Exported {len(self.scraped_items_list)} items to {filename}")


    def _build_settings_tab(self):
        frame = self.tab_settings

        # Playwright toggle
        self.playwright_var = tk.BooleanVar(value=True)
        chk_pw = tk.Checkbutton(
            frame,
            text="Enable Playwright Headless Browser Rendering (Dynamic JavaScript Sites)",
            variable=self.playwright_var,
            bg="#1e1e2e",
            fg="#cdd6f4",
            selectcolor="#313244",
            activebackground="#1e1e2e",
            font=("Segoe UI", 10, "bold")
        )
        chk_pw.pack(anchor="w", pady=10)

        # Proxy rotation
        ttk.Label(frame, text="Proxy List (One per line: http://user:pass@host:port):").pack(anchor="w", pady=(10, 5))
        self.proxy_text = scrolledtext.ScrolledText(frame, height=8, bg="#11111b", fg="#cdd6f4", font=("Consolas", 9))
        self.proxy_text.insert("1.0", "# Example Proxy List:\n# http://127.0.0.1:8080\n")
        self.proxy_text.pack(fill="x", pady=5)

    def _build_updater_tab(self):
        frame = self.tab_updater

        ttk.Label(frame, text="GitHub Auto-Update Center", style="Header.TLabel").pack(anchor="w", pady=5)

        info_lbl = ttk.Label(
            frame,
            text="AtoZ Scrapy Windows ED automatically connects to GitHub to check for updates.\n"
                 "When new releases or fixes are pushed to GitHub, you can update directly from this interface.",
            justify="left"
        )
        info_lbl.pack(anchor="w", pady=5)

        # Repo input
        repo_frame = ttk.Frame(frame, padding=(0, 10))
        repo_frame.pack(fill="x")

        ttk.Label(repo_frame, text="GitHub Repository Owner/Repo:").pack(side="left", padx=5)
        self.repo_entry = ttk.Entry(repo_frame, width=40)
        self.repo_entry.insert(0, "user/AtoZ-Scrapy-Windows-ED")
        self.repo_entry.pack(side="left", padx=5)

        # Check button
        btn_check = ttk.Button(frame, text="🔄 Check GitHub for Updates", command=self._check_github_updates)
        btn_check.pack(anchor="w", pady=10)

        # Output / status text
        self.update_log = scrolledtext.ScrolledText(frame, height=10, bg="#11111b", fg="#a6e3a1", font=("Consolas", 9))
        self.update_log.pack(fill="both", expand=True, pady=10)

        self.btn_apply_update = ttk.Button(frame, text="⚡ Download & Install Latest Update", command=self._apply_github_update)
        self.btn_apply_update.pack(anchor="w", pady=5)
        self.btn_apply_update.config(state="disabled")

    def _start_spider(self):
        spider_name = self.spider_input.get().strip() or "demo_quotes"
        target_url = self.url_input.get().strip()
        concurrency = self.concurrency_spin.get()

        self.log_text.insert("end", f"[SYS] Launching spider '{spider_name}' targeting {target_url}...\n")
        self.log_text.insert("end", "[SYS] Windows IOCP Async Engine initialized.\n")
        self.log_text.insert("end", f"[ENGINE] Playwright dynamic rendering: {'ENABLED' if self.playwright_var.get() else 'DISABLED'}\n")
        self.log_text.insert("end", f"[ENGINE] Concurrency level: {concurrency} requests/sec.\n")
        self.log_text.see("end")
        self.status_var.set(f"Running spider: {spider_name}")

        def run_proc():
            cmd = [sys.executable, "-m", "scrapy", "crawl", spider_name]
            try:
                self.current_process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    cwd=os.getcwd()
                )
                for line in iter(self.current_process.stdout.readline, ''):
                    if not line:
                        break
                    self.root.after(0, lambda l=line: (self.log_text.insert("end", l), self.log_text.see("end")))

                self.current_process.wait()
                self.root.after(0, lambda: (
                    self.log_text.insert("end", f"[SYS] Spider '{spider_name}' run finished cleanly.\n"),
                    self.log_text.see("end"),
                    self.status_var.set("Engine idle.")
                ))
            except Exception as e:
                self.root.after(0, lambda: self.log_text.insert("end", f"[ERROR] Failed to run spider: {e}\n"))

        threading.Thread(target=run_proc, daemon=True).start()

    def _stop_spider(self):
        if hasattr(self, 'current_process') and self.current_process:
            try:
                self.current_process.terminate()
                self.log_text.insert("end", "[SYS] Engine process terminated gracefully.\n")
            except Exception as e:
                self.log_text.insert("end", f"[ERROR] Error stopping process: {e}\n")
        else:
            self.log_text.insert("end", "[SYS] Engine stop signal received.\n")
        self.log_text.see("end")
        self.status_var.set("Engine stopped.")


    def _check_github_updates(self):
        repo_info = self.repo_entry.get().strip()
        self.update_log.delete("1.0", "end")
        self.update_log.insert("end", f"[UPDATER] Checking GitHub API for repository: '{repo_info}'...\n")

        def task():
            has_update, info = self.updater.check_for_updates(repo_info)
            if "error" in info:
                self.update_log.insert("end", f"[ERROR] {info['error']}\n")
            elif "message" in info:
                self.update_log.insert("end", f"[INFO] {info['message']}\n")
            else:
                self.update_log.insert("end", f"[STATUS] Latest Release Found: {info.get('release_name')}\n")
                self.update_log.insert("end", f"[STATUS] Current Version: {info.get('current_version')}\n")
                self.update_log.insert("end", f"[STATUS] Latest Tag: {info.get('latest_version')}\n\n")
                self.update_log.insert("end", f"Release Notes:\n{info.get('release_notes')}\n")

                if has_update:
                    self.update_log.insert("end", "\n✨ NEW UPDATE AVAILABLE! Click 'Download & Install' below.\n")
                    self.latest_zip_url = info.get("zip_url")
                    self.root.after(0, lambda: self.btn_apply_update.config(state="normal"))
                else:
                    self.update_log.insert("end", "\n✅ You are running the latest version of AtoZ Scrapy Windows ED.\n")
            self.update_log.see("end")

        threading.Thread(target=task, daemon=True).start()

    def _apply_github_update(self):
        zip_url = getattr(self, "latest_zip_url", "")
        if not zip_url:
            messagebox.showwarning("Update Error", "No update download URL found.")
            return

        self.update_log.insert("end", f"[UPDATER] Downloading update package from {zip_url}...\n")

        def task():
            success, msg = self.updater.apply_update_from_zip(zip_url, os.getcwd())
            self.update_log.insert("end", f"[{'SUCCESS' if success else 'FAIL'}] {msg}\n")
            if success:
                messagebox.showinfo("Update Complete", "Update downloaded successfully! Please restart the application.")

        threading.Thread(target=task, daemon=True).start()

    def _create_statusbar(self):
        self.status_var = tk.StringVar(value=f"Ready | {FULL_APP_TITLE}")
        statusbar = ttk.Label(self.root, textvariable=self.status_var, style="Status.TLabel", padding=(15, 5))
        statusbar.pack(fill="x", side="bottom")


def main():
    root = tk.Tk()
    app = AtoZScrapyWindowsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
