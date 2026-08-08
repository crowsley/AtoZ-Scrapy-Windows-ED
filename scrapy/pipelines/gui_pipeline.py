"""
AtoZ Scrapy Windows ED 0.0.1 - GUI Item Pipeline

Receives items scraped by spiders and streams them into a thread-safe Queue
for real-time display in the Windows Desktop GUI Treeview table.
"""

import queue
import time

# Thread-safe global queue for GUI item streaming
GUI_ITEM_QUEUE = queue.Queue()


class GuiItemPipeline:
    """
    Scrapy pipeline that pushes item dictionaries to the GUI queue.
    """

    def process_item(self, item, spider):
        item_dict = dict(item) if hasattr(item, "keys") else item
        timestamp = time.strftime("%H:%M:%S")

        payload = {
            "spider": spider.name,
            "url": item_dict.get("url") or item_dict.get("link") or item_dict.get("title") or "N/A",
            "content": str(item_dict)[:120],
            "timestamp": timestamp,
            "raw_item": item_dict
        }

        GUI_ITEM_QUEUE.put(payload)
        return item
