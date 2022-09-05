from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as undchromedriver
import pathlib


class Webcreate(object):

    def _driverinit(self):
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        chrome_driver_path = str(pathlib.Path(__file__).parent.absolute()) + '/chromedriver.exe'
        chrome_options = Options()
        # chrome_options.add_argument('headless')
        driver = undchromedriver.Chrome(options=chrome_options, executable_path=chrome_driver_path)
        driver.set_window_position(0, 0)
        driver.set_window_size(1920, 1080)
        return driver