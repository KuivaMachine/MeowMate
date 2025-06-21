import sys
from pathlib import Path

import requests
import json
import os
import subprocess


VERSION_URL = "https://raw.githubusercontent.com/KuivaMachine/MeowMate/refs/heads/main/version.json"
APPDIR = Path(sys.executable).parent
CURRENT_VERSION = "1.0.0"

def check_update():
    print(APPDIR)
    CURRENT_VERSION = load_settings(os.path.join(APPDIR, "version.json"))["version"]
    print(CURRENT_VERSION)
    response = requests.get(VERSION_URL)
    remote_data = json.loads(response.text)
    print(remote_data["version"])
    if remote_data["version"] != CURRENT_VERSION:
        print("Версии не равны, качаю новую")
        return remote_data["download_url"]
    else:
        print("Обновлений нет")
        return None


def load_settings(path):
    try:
        with open(path, "r", encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Файл не найден или поврежден")
        return None

def download_and_install(url):
    update_file = os.path.join(APPDIR, "MeowMate_update.exe")
    print(f"начинаю качать в {update_file}")
    with requests.get(url, stream=True) as r:
        with open(update_file, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    subprocess.run([update_file, "/quiet"], shell=True)
    os.remove(update_file)


if __name__ == "__main__":
    update_url = (check_update())
    if update_url:
        download_and_install(update_url)