from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import re
from selenium.webdriver.support import expected_conditions as EC


class Helper():

    def __init__(self, driver, test_logger):
        self.driver = driver
        self.test_logger = test_logger
        self.actions = ActionChains(driver)

    def go_to_page(self, url):
        self.test_logger.info(f"Navigate to {url}")
        self.driver.get(url)
        self.driver.maximize_window()

    def find_and_click(self, loc, timeout=30):
        elem = self.find(loc, timeout)
        elem.click()

    def find_and_send_keys(self, loc, inp_text, timeout=10):
        elem = self.find(loc, timeout)
        elem.send_keys(inp_text)

    def find(self, loc, timeout=20, should_exist=True, get_text="", get_attribute=""):
        try:
            elem = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(loc),
                message=f"Element '{loc}' not found!")
        except Exception as e:
            self.test_logger.error(e)
            if should_exist:
                raise Exception(e)
            return False
        if get_text:
            self.test_logger.info(f"Element text: {elem.text}")
            return elem.text
        elif get_attribute:
            return elem.get_attribute(get_attribute)
        return elem

    def find_all(self, loc, timeout=10):
        try:
            elements = WebDriverWait(self.driver, timeout).\
                until(EC.presence_of_all_elements_located(loc),
                      message=f"Elements '{loc}' not found!")
        except Exception as e:
            self.test_logger.error(e)
            return False
        return elements

    def wait_element_disappear(self, loc, timeout=10):
        WebDriverWait(self.driver, timeout).until_not(EC.presence_of_element_located(loc))
    
    def wait_element_clickable(self, loc, timeout=30):
        WebDriverWait(self.driver, timeout).until_not(EC.element_to_be_clickable(loc))

    def wait_for_page(self, page="", not_page="", timeout=10):
        if page:
            WebDriverWait(self.driver, timeout).until(EC.url_contains(page))
        elif not_page:
            WebDriverWait(self.driver, timeout).until_not(EC.url_contains(not_page))

    def hover_element(self, loc):
        hover = self.actions.move_to_element(self.find(loc)).pause(0.5)
        hover.perform()

    def wait_for_page_load(self, timeout=30):
        self.driver.set_page_load_timeout(timeout)

    # make locator dynamic
    def remake_locator(self, *args):
        return args[0][0], args[0][1] % args[1]
    