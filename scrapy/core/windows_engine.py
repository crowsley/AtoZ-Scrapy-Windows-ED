"""
AtoZ Scrapy Windows ED 0.0.1 - Windows High-Concurrency Engine

Configures Windows Proactor I/O event loop harness and multi-process worker pool.
"""

import sys
import asyncio
from scrapy.utils.reactor import install_reactor


def configure_windows_engine():
    """
    Sets up the optimal asyncio event loop policy for Windows (Proactor/IOCP).
    """
    if sys.platform == "win32":
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        except AttributeError:
            pass

    # Ensure Scrapy uses asyncio reactor
    try:
        install_reactor("twisted.internet.asyncioreactor.AsyncioSelectorReactor")
    except Exception:
        pass
