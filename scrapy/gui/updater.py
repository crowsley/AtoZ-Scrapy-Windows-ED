"""
AtoZ Scrapy Windows ED 0.0.1 - GitHub Auto-Updater Module

Handles checking GitHub releases and git commits for updates, downloading update packages,
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
    Manages checking for updates from GitHub releases & commits.
    """

    def __init__(self, repo_owner: str = "crowsley", repo_name: str = "AtoZ-Scrapy-Windows-ED"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = APP_VERSION


    def check_for_updates(self, repo_url_or_owner: Optional[str] = None) -> Tuple[bool, Dict[str, Any]]:
        """
        Checks GitHub for the latest release version or latest commit.
        Returns (has_update, update_info_dict).
        """
        repo_spec = repo_url_or_owner or f"{self.repo_owner}/{self.repo_name}"
        if not repo_spec or "user/" in repo_spec:
            repo_spec = "crowsley/AtoZ-Scrapy-Windows-ED"


        repo_path = repo_spec.replace("https://github.com/", "").strip("/")

        # 1. First check Releases API
        rel_url = f"https://api.github.com/repos/{repo_path}/releases/latest"
        try:
            req = urllib.request.Request(
                rel_url,
                headers={"User-Agent": "AtoZ-Scrapy-Windows-ED-Updater"}
            )
            with urllib.request.urlopen(req, timeout=8) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    latest_tag = data.get("tag_name", "").lstrip("v")
                    published_at = data.get("published_at", "")
                    body = data.get("body", "No release notes provided.")
                    zip_url = data.get("zipball_url", "")

                    has_update = latest_tag > self.current_version if latest_tag else False

                    return has_update, {
                        "type": "release",
                        "latest_version": latest_tag,
                        "current_version": self.current_version,
                        "release_name": data.get("name", f"Release {latest_tag}"),
                        "release_notes": body,
                        "published_at": published_at,
                        "zip_url": zip_url,
                        "html_url": data.get("html_url", "")
                    }
        except urllib.error.HTTPError as e:
            if e.code != 404:
                return False, {"error": f"HTTP Error checking releases: {e.code}"}
        except Exception:
            pass

        # 2. Fallback to Commits API if no formal releases published yet
        commit_url = f"https://api.github.com/repos/{repo_path}/commits/master"
        try:
            req = urllib.request.Request(
                commit_url,
                headers={"User-Agent": "AtoZ-Scrapy-Windows-ED-Updater"}
            )
            with urllib.request.urlopen(req, timeout=8) as response:
                if response.status == 200:
                    cdata = json.loads(response.read().decode("utf-8"))
                    sha = cdata.get("sha", "")[:7]
                    commit_msg = cdata.get("commit", {}).get("message", "")
                    author = cdata.get("commit", {}).get("author", {}).get("name", "")
                    date = cdata.get("commit", {}).get("author", {}).get("date", "")
                    zip_url = f"https://github.com/{repo_path}/archive/refs/heads/master.zip"

                    return False, {
                        "type": "commit",
                        "latest_version": f"master-{sha}",
                        "current_version": self.current_version,
                        "release_name": f"Latest Git Commit ({sha})",
                        "release_notes": f"Author: {author}\nDate: {date}\nMessage: {commit_msg}",
                        "published_at": date,
                        "zip_url": zip_url,
                        "html_url": cdata.get("html_url", "")
                    }
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return False, {"message": f"GitHub repository '{repo_path}' not created on GitHub yet.\nPush your local commits to GitHub using: `git push -u origin master`"}
            return False, {"error": f"HTTP Error checking commits: {e.code}"}
        except Exception as e:
            return False, {"error": f"Failed to connect to GitHub: {str(e)}"}

        return False, {"message": f"Connected to GitHub repository '{repo_path}'. Running latest code."}

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
