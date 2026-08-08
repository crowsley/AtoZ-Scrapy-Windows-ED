"""
AtoZ Scrapy Windows ED 0.0.1 - Command Line Interface (CLI)

Provides command-line commands for launching the Windows Desktop GUI,
checking updates, and running spiders.
"""

import sys
import argparse
from .version import FULL_APP_TITLE, APP_VERSION
from .updater import GitHubUpdater


def main():
    parser = argparse.ArgumentParser(
        prog="atoz-scrapy",
        description=f"{FULL_APP_TITLE} - High-Performance Windows Web Scraping Suite"
    )
    parser.add_argument("-v", "--version", action="version", version=FULL_APP_TITLE)

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command 1: gui
    subparsers.add_parser("gui", help="Launch the AtoZ Scrapy Windows Desktop GUI")

    # Command 2: update
    update_parser = subparsers.add_parser("update", help="Check for GitHub updates")
    update_parser.add_argument("--repo", type=str, default="", help="GitHub owner/repo")

    args = parser.parse_args()

    if args.command == "gui" or not args.command:
        import tkinter as tk
        from .main_gui import AtoZScrapyWindowsApp
        root = tk.Tk()
        app = AtoZScrapyWindowsApp(root)
        root.mainloop()

    elif args.command == "update":
        print(f"[{FULL_APP_TITLE}] Checking GitHub API for updates...")
        updater = GitHubUpdater()
        has_update, info = updater.check_for_updates(args.repo)
        if "error" in info:
            print(f"Error: {info['error']}")
        elif "message" in info:
            print(f"Info: {info['message']}")
        else:
            print(f"Latest Release: {info.get('release_name')}")
            print(f"Current Version: {info.get('current_version')}")
            print(f"Latest Tag: {info.get('latest_version')}")
            if has_update:
                print("\n✨ NEW UPDATE AVAILABLE! Download from GitHub releases or run 'atoz-scrapy gui'.")
            else:
                print("\n✅ Up to date!")


if __name__ == "__main__":
    main()
