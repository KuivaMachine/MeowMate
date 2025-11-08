import datetime
import json
import os
import platform
import subprocess
import sys
from getpass import getuser
from pathlib import Path, WindowsPath

import requests
from PyQt5.QtCore import QThread, pyqtSignal
from dotenv import load_dotenv

from utils.utils import log_error


def load_settings(path):
    try:
        with open(path, "r", encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Файл не найден или поврежден")
        return None

def send_statistic(url, kiwi, version):
    system_info = (
        f"Установлена и запущена MeowMate v{version}\n"
        f"⏰ Время: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"👤 Пользователь: {getuser()}\n"
        f"💻 Система: {platform.system()} {platform.version()}\n"
        f"🖥️ Имя ПК: {platform.node()}"
    )

    payload = {
        "chat_id": kiwi,
        "text": system_info,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Статистика отправлена")
        else:
            log_error(response.text, "send_statistic")
            print(f"Ошибка: {response.text}")
    except Exception as e:
        log_error(str(e), "send_statistic")
        print(f"Ошибка соединения: {str(e)}")

def is_new_version(github_version, current_version):
    return int(github_version.replace(".", ""))>int(current_version.replace(".", ""))


class UpdatesChecker(QThread):
    update_available = pyqtSignal(str, str)

    def __init__(self,is_first_run):
        super().__init__()

        self.VERSION_URL = "https://raw.githubusercontent.com/KuivaMachine/MeowMate/refs/heads/main/version.json"
        self.APPDIR = Path(sys.executable).parent # ДЛЯ РЕЛИЗА
        # self.APPDIR = "./" # ДЛЯ ЛОКАЛЬНОГО ЗАПУСКА
        self.is_first_run = is_first_run

    def run(self):

        current_version = load_settings(os.path.join(self.APPDIR, "version.json"))["version"]

        try:
            if self.is_first_run:
                load_dotenv(self.APPDIR / '_internal' / './resources' / '.env')  # ДЛЯ РЕЛИЗА
                # load_dotenv('./resources/.env') # ДЛЯ ЛОКАЛЬНОГО ЗАПУСКА
                send_statistic(os.getenv("apple"), os.getenv("kiwi"), current_version)

            response = requests.get(self.VERSION_URL)
            data_from_github = json.loads(response.text)
            github_version = data_from_github["version"]
            if is_new_version(github_version,current_version):
                print(f"Есть новая версия - {github_version}. Старая - {current_version}")
                self.update_available.emit(data_from_github["version"], data_from_github["download_url"])
            else:
                print("Обновлений нет")
                return None
        except requests.ConnectionError:
            log_error("Нет интернета", "UpdatesChecker.run")
            print("Нет интернета (requests.ConnectionError)")
        except requests.Timeout:
            log_error("Таймаут соединения", "UpdatesChecker.run")
            print("Таймаут соединения")
        except requests.HTTPError as e:
            log_error("HTTP ошибка",e.response.status_code, "UpdatesChecker.run" )
            print(f"HTTP ошибка: {e.response.status_code}")
        except Exception as e:
            log_error("Ошибка загрузки", str(e), "UpdatesChecker.run" )
            print(f"Ошибка загрузки: {str(e)}")
        finally:
            return None


class UpdatesDownloader(QThread):
    progress_updated = pyqtSignal(int)
    download_finished = pyqtSignal(WindowsPath)

    def __init__(self, parent, download_url):
        super().__init__()
        self.download_url = download_url
        self.parent = parent

    def run(self):
        download_dir = Path(os.getenv('ProgramData')) / 'MeowMate'
        download_dir.mkdir(parents=True, exist_ok=True)
        update_file = download_dir / "MeowMate_update.exe"

        try:
                with requests.get(self.download_url, stream=True) as r:
                    #Проверяет, был ли HTTP-запрос успешным. Если сервер вернул ошибку (например, 404 или 500), метод выбросит исключение. Это предотвращает попытки работы с битым файлом
                    r.raise_for_status()

                    # Получаем общий размер файла из заголовков
                    total_size = int(r.headers.get('content-length', 0))

                    if update_file.exists() and update_file.stat().st_size==total_size:
                        print("Найдено свежее загруженное обновление")
                        self.progress_updated.emit(100)
                        self.download_finished.emit(update_file)

                    else:
                        print(f"Файла обновлений нет. Скачиваю новую версию в {download_dir}")
                        downloaded_size = 0
                        progress_buffer = 0
                        with open(update_file, "wb") as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                                    downloaded_size += len(chunk)
                                    if total_size > 0:
                                        progress = int((downloaded_size / total_size) * 100)
                                        if progress > progress_buffer and progress % 10 == 0:
                                            self.progress_updated.emit(progress)
                                            progress_buffer = progress

                        self.download_finished.emit(update_file)

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



class UpdatesInstaller(QThread):
    install_finished = pyqtSignal()

    def __init__(self, update_file):
        super().__init__()
        self.update_file = str(update_file)

    def run(self):
        ps_script = f"""Stop-Process -Name "MeowMate" -Force
                       Start-Process "{self.update_file}" -ArgumentList "/quiet", "/norestart" -Verb RunAs -Wait
                       Start-Process "{Path(sys.executable).parent}\\MeowMate.exe"
                       Remove-Item -Path "{self.update_file}" -Force"""


        subprocess.run([
            "powershell.exe",
            "-ExecutionPolicy", "Bypass",
            "-Command", ps_script
        ], creationflags=subprocess.CREATE_NO_WINDOW, check=True)
