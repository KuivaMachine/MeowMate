import sys
from pathlib import Path

import requests
import json
import os
import subprocess

from PyQt5.QtCore import QThread, pyqtSignal


def load_settings(path):
    try:
        with open(path, "r", encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Файл не найден или поврежден")
        return None


class UpdatesChecker(QThread):
    update_available = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.VERSION_URL = "https://raw.githubusercontent.com/KuivaMachine/MeowMate/refs/heads/main/version.json"
        self.APPDIR = Path(sys.executable).parent
        # self.APPDIR = "./"

    def run(self):
        print(self.APPDIR)
        CURRENT_VERSION = load_settings(os.path.join(self.APPDIR, "version.json"))["version"]
        print(CURRENT_VERSION)
        try:
            response = requests.get(self.VERSION_URL)
            remote_data = json.loads(response.text)
            print(remote_data["version"])
            if remote_data["version"] != CURRENT_VERSION:
                print("Версии не равны")
                self.update_available.emit(remote_data["download_url"])
            else:
                print("Обновлений нет")
                return None
        except requests.ConnectionError:
            print("Ошибка подключения")
        except requests.Timeout:
            print("Таймаут соединения")
        except requests.HTTPError as e:
           print(f"HTTP ошибка: {e.response.status_code}")
        except Exception as e:
            print(f"Ошибка загрузки: {str(e)}")
        finally:
            return None


class UpdatesDownloader(QThread):
    def __init__(self, download_url):
        super().__init__()
        self.download_url = download_url

    def run(self):
        download_dir =  Path(os.getenv('ProgramData')) / 'MeowMate'
        download_dir.mkdir(parents=True, exist_ok=True)
        update_file = download_dir / "MeowMate_update.exe"
        if not update_file.exists():
            print(f"Начинаю скачивать в {download_dir}")
            try:
                with requests.get(self.download_url, stream=True) as r:
                    with open(update_file, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
            except requests.ConnectionError:
                print("Ошибка подключения")
                return None
            except requests.Timeout:
                print("Таймаут соединения")
                return None
            except requests.HTTPError as e:
               print(f"HTTP ошибка: {e.response.status_code}")
               return None
            except Exception as e:
                print(f"Ошибка загрузки: {str(e)}")
                return None



        print("Скачал, устанавливаю...")
        subprocess.run([update_file, "/quiet"], shell=True)
        print("Закончил")
        os.remove(update_file)
        print("Удалил")
