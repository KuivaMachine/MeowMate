import sys
import tempfile
from pathlib import Path

import requests
import json
import os
import subprocess

from PyQt5.QtCore import QThread, pyqtSignal


class UpdatesChecker(QThread):
    update_available = pyqtSignal(str)
    download_complete = pyqtSignal()


    def __init__(self):
        super().__init__()

        self.VERSION_URL = "https://raw.githubusercontent.com/KuivaMachine/MeowMate/refs/heads/main/version.json"
        # self.APPDIR = Path(sys.executable).parent
        self.APPDIR = "./"

    def run(self):
        print(self.APPDIR)
        CURRENT_VERSION = self.load_settings(os.path.join(self.APPDIR, "version.json"))["version"]
        print(CURRENT_VERSION)
        response = requests.get(self.VERSION_URL)
        remote_data = json.loads(response.text)
        print(remote_data["version"])
        if remote_data["version"] != CURRENT_VERSION:
            print("Версии не равны, качаю новую")
            self.update_available.emit(remote_data["download_url"])
        else:
            print("Обновлений нет")
            return None


    def load_settings(self, path):
        try:
            with open(path, "r", encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Файл не найден или поврежден")
            return None

    def download_and_install(self,download_url):
        update_file = os.path.join(tempfile.gettempdir(), "MeowMate_update.exe")
        print(f"Начинаю скачивать в {update_file}")
        with requests.get(download_url, stream=True) as r:
            with open(update_file, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print("Скачал, устанавливаю...")
        subprocess.run([update_file, "/quiet"], shell=True)
        os.remove(update_file)


