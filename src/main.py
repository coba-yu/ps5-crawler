import os
import re
import shutil
from tempfile import TemporaryDirectory

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from line.notify import LineNotifier

HIKARI_TV_URL = "https://shop.hikaritv.net/"


def is_about_ps5(s: str) -> bool:
    return re.search(r"playstation5|ps5", s.lower()) is not None


def run(driver_path: str) -> None:
    driver = Chrome(driver_path)
    driver.get(HIKARI_TV_URL)
    try:
        elements = driver.find_elements(By.XPATH, "//*[@class='recommendImg']")
        for e in elements:
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
    print("args:", args)
    print("kwargs:", kwargs)
    driver_file_name = "chromedriver"
    with TemporaryDirectory() as tmp_dir:
        tmp_driver_path = os.path.join(tmp_dir, driver_file_name)
        shutil.copyfile(
            src=os.path.join(os.getcwd(), driver_file_name),
            dst=tmp_driver_path,
        )
        os.chmod(tmp_driver_path, 755)
        run(driver_path=tmp_driver_path)


# if __name__ == '__main__':
#     main()
