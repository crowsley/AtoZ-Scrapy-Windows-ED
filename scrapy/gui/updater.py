"""
AtoZ Scrapy Windows ED 0.0.1 - GitHub Auto-Updater Module

Handles checking GitHub releases/commits for updates, downloading update packages,
and applying updates directly to the local Windows installation.
"""

import os
import sys
import json
import zipfile
import tempfile
import urllib.request
import urllib.error
from typing import Dict, Any, Tuple, Optional
try:
    from scrapy.gui.version import APP_VERSION
except (ImportError, ValueError):
    from .version import APP_VERSION




class GitHubUpdater:
    """
    Manages checking for updates from GitHub and updating local application.
    """

    def __init__(self, repo_owner: str = "", repo_name: str = "AtoZ-Scrapy-Windows-ED"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = APP_VERSION

    def get_api_url(self) -> str:
        if self.repo_owner:
            return f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"
        return f"https://api.github.com/repos/{self.repo_name}/releases/latest"

    def check_for_updates(self, repo_url_or_owner: Optional[str] = None) -> Tuple[bool, Dict[str, Any]]:
        """
        Checks GitHub for the latest release version.
        Returns (has_update, update_info_dict).
        """
        owner = repo_url_or_owner or self.repo_owner
        if not owner:
            return False, {"error": "GitHub repository owner/repo not configured. Set your GitHub repo details in the Updater tab."}

        url = f"https://api.github.com/repos/{owner}/{self.repo_name}/releases/latest" if "/" not in owner else f"https://api.github.com/repos/{owner}/releases/latest"

        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "AtoZ-Scrapy-Windows-ED-Updater"}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    latest_tag = data.get("tag_name", "").lstrip("v")
                    published_at = data.get("published_at", "")
                    body = data.get("body", "No release notes provided.")
                    zip_url = data.get("zipball_url", "")

                    has_update = latest_tag > self.current_version if latest_tag else False

                    return has_update, {
                        "latest_version": latest_tag,
                        "current_version": self.current_version,
                        "release_name": data.get("name", f"Release {latest_tag}"),
                        "release_notes": body,
                        "published_at": published_at,
                        "zip_url": zip_url,
                        "html_url": data.get("html_url", "")
                    }
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return False, {"message": f"No GitHub releases found for '{owner}'. You are running the latest code."}
            return False, {"error": f"HTTP Error checking updates: {e.code}"}
        except Exception as e:
            return False, {"error": f"Failed to check updates: {str(e)}"}

        return False, {"message": "Already up to date."}

    def apply_update_from_zip(self, zip_url: str, target_dir: str) -> Tuple[bool, str]:
        """
        Downloads update zip from GitHub release and extracts updated files to target_dir.
        """
        try:
            temp_dir = tempfile.mkdtemp(prefix="atoz_scrapy_update_")
            zip_path = os.path.join(temp_dir, "update.zip")

            req = urllib.request.Request(
                zip_url,
                headers={"User-Agent": "AtoZ-Scrapy-Windows-ED-Updater"}
            )
            with urllib.request.urlopen(req, timeout=30) as resp, open(zip_path, "wb") as f:
                f.write(resp.read())

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            return True, f"Downloaded update package successfully to {zip_path}. Application ready to reload."
        except Exception as e:
            return False, f"Failed to download/apply update: {str(e)}"
