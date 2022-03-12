import os
import re
import shutil
from pathlib import Path
from stat import S_IXGRP, S_IXUSR
from tempfile import TemporaryDirectory
from traceback import format_exc

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from line.notify import LineNotifier

HIKARI_TV_URL = "https://shop.hikaritv.net/"


def add_execute_permission(path: Path) -> None:
    path.chmod(mode=path.stat().st_mode | S_IXUSR | S_IXGRP)


def prepare_selenium_file(file_name: str, tmp_dir: str) -> str:
    path = os.path.join(tmp_dir, file_name)
    shutil.copyfile(src=os.path.join(os.getcwd(), file_name), dst=path)
    add_execute_permission(path=Path(path))
    os.chmod(path, 0o755)
    return path


def is_about_ps5(s: str) -> bool:
    return re.search(r"playstation5|ps5", s.lower()) is not None


def run(driver_path: str, chromium_path: str = None) -> None:
    options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")
    # options.add_argument("--window-size=1280x1696")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--hide-scrollbars")
    # options.add_argument("--enable-logging")
    # options.add_argument("--log-level=0")
    # options.add_argument("--v=99")
    # options.add_argument("--single-process")
    # options.add_argument("--ignore-certificate-errors")
    # options.add_argument("--disable-dev-shm-usage")
    if chromium_path is not None:
        options.binary_location = chromium_path
    driver = Chrome(
        service=Service(executable_path=driver_path),
        options=options,
    )
    driver.get(HIKARI_TV_URL)
    try:
        elements = driver.find_elements(By.XPATH, "//*[@class='recommendImg']")
        for e in elements:
            if type(e) == type(dict):
                # dict の場合, element が見つかっていないので skip
                continue
            alt = e.get_attribute("alt")
            if is_about_ps5(alt):
                LineNotifier.notify(message="\n".join((
                    alt,
                    HIKARI_TV_URL,
                )))
                return
    finally:
        driver.close()


def main(*args, **kwargs):
    response = {"args": args, "kwargs": kwargs}
    try:
        with TemporaryDirectory() as tmp_dir:
            tmp_driver_path = prepare_selenium_file(file_name="chromedriver", tmp_dir=tmp_dir)
            tmp_chromium_path = prepare_selenium_file(file_name="headless-chromium", tmp_dir=tmp_dir)
            response["tmp_driver_path"] = tmp_driver_path
            response["tmp_chromium_path"] = tmp_chromium_path
            run(driver_path=tmp_driver_path, chromium_path=tmp_chromium_path)
    except Exception:
        response["exception"] = format_exc()
    finally:
        print(response)
        return str(response)


if __name__ == '__main__':
    driver_path = "../chromedriver_mac64"
    os.chmod(driver_path, 0o755)
    run(driver_path=driver_path)
