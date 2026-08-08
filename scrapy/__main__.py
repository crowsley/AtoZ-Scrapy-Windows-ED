# pragma: no file cover
"""
AtoZ Scrapy Windows ED 0.0.1 - Main Entry Point

Running `python -m scrapy` opens the Windows Desktop Application GUI directly.
"""

import sys

def main():
    # If subcommand is explicitly passed (e.g., `python -m scrapy crawl`), fallback to CLI
    if len(sys.argv) > 1 and sys.argv[1] not in ["gui", "--gui"]:
        from scrapy.cmdline import execute
        execute()
    else:
        import tkinter as tk
        from scrapy.gui.main_gui import AtoZScrapyWindowsApp
        root = tk.Tk()
        app = AtoZScrapyWindowsApp(root)
        root.mainloop()

if __name__ == "__main__":
    main()
