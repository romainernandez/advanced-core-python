import requests
import os
import json
import hashlib
import time
from urllib.parse import urljoin

WATCHED_EXTS = [".py"]
IGNORE_DIRS = [".git"]


ASCII_ART = """
  _____ _    _ _ _            __          ___           _
 / ____| |  (_) | |           \\ \\        / / |         | |
| (___ | | ___| | | ___ _ __   \\ \\  /\\  / /| |__   __ _| | ___
 \\___ \\| |/ / | | |/ _ \\ '__|   \\ \\/  \\/ / | '_ \\ / _` | |/ _ \\
 ____) |   <| | | |  __/ |       \\  /\\  /  | | | | (_| | |  __/
|_____/|_|\\_\\_|_|_|\\___|_|        \\/  \\/   |_| |_|\\__,_|_|\\___|

"""


SERVER_URL = os.getenv('SERVER_URL', "https://train.skillerwhale.com")


def create_skiller_whale_url(path):
    return urljoin(SERVER_URL, path)


class Updater:
    def __init__(self, attendance_id):
        self.attendance_id = attendance_id

    @property
    def uri(self):
        return create_skiller_whale_url(self.path)

    @property
    def path(self):
        return f'attendances/{self.attendance_id}/file_snapshots'

    @staticmethod
    def get_file_data(path):
        with open(path, "r") as f:
            data ={"relative_path": path, "contents": f.read()}
            return json.dumps(data)

    @staticmethod
    def get_headers(data):
        return {
            "Content-Type": "application/json",
            "Content-Length": str(len(data))
        }

    def post_file(self, path):
        data = self.get_file_data(path)
        headers = self.get_headers(data)
        return requests.post(self.uri, data=data, headers=headers)

    def send_file_update(self, path):
        print(f"Uploading: {path}", end='\t')
        if not self.attendance_id:
            print("No attendance id set; file update not sent.")
            return

        response = self.post_file(path)
        print(f"Status: {response.status_code}")

        if response.text:
            print(response.text)


class Pinger:
    def __init__(self, attendance_id):
        self.attendance_id = attendance_id

    @property
    def uri(self):
        return create_skiller_whale_url(self.path)

    @property
    def path(self):
        return f'attendances/{self.attendance_id}/pings'

    def ping(self):
        requests.post(self.uri)


class Watcher:
    def __init__(self, updater, pinger, base_path='.'):
        self.updater = updater
        self.pinger = pinger
        self.base_path = base_path
        self._file_hashes = {}
        # Tracks whether this is the first pass of the directory tree. If not,
        # then any new file encountered will be treated as an update.
        self._first_pass = True

    @staticmethod
    def get_file_hash(path):
        """Return a hash digest of the file located at path"""
        with open(path, "rb") as f:
            contents = f.read()
            return hashlib.md5(contents).hexdigest()

    def _post_file_if_changed(self, path):
        _, extension = os.path.splitext(path)
        if extension not in WATCHED_EXTS:
            return

        hashed = self.get_file_hash(path)
        if not self._first_pass:
            old_hash = self._file_hashes.get(path)
            if old_hash != hashed:
                self.updater.send_file_update(path)
        self._file_hashes[path] = hashed

    def _check_dir_for_changes(self, dir_path):
        if os.path.basename(dir_path) in IGNORE_DIRS:
            return

        for filename in os.listdir(dir_path):
            new_path = os.path.join(dir_path, filename)
            if os.path.isdir(new_path):
                # Recursively check subdirectories
                self._check_dir_for_changes(new_path)
            else:
                self._post_file_if_changed(new_path)

    def poll_for_changes(self, wait_time=1):
        while True:
            self.pinger.ping()
            self._check_dir_for_changes(self.base_path)
            self._first_pass = False
            time.sleep(wait_time)  # Poll for changes every `wait_time` seconds


def skiller_whale_sync():
    print(ASCII_ART)
    attendance_id = input("Please copy and paste your ID from the course "
                          "page here and press enter.\n")
    print("")
    print("Great! We're going to start watching this directory for changes "
          "so that the trainer can see your progress.")
    print("Hit Ctrl+C to stop.")

    updater = Updater(attendance_id=attendance_id)
    pinger = Pinger(attendance_id=attendance_id)
    watcher = Watcher(updater=updater, pinger=pinger)
    watcher.poll_for_changes()


if __name__ == "__main__":
    skiller_whale_sync()
