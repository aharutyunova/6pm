from selenium.webdriver.common.by import By
from Helpers.helpers_lib import Helper
import logging
from TestData import search_filters
import re

class SearchPage(Helper):

    txt_search_field = (By.XPATH, "//input[@id='searchAll']")
    search_loopa = (By.XPATH, "//*[@id='searchForm']/button")
    btn_brand = (By.XPATH, "//button[@data-selected-facet-group-name='brandNameFacet']")
    chb_shop_by_brand = (By.XPATH, "//ul[@aria-labelledby='brandNameFacet']//span[text()='%s']")
    btn_price = (By.XPATH, "//button[@data-selected-facet-group-name='priceFacet']")
    chb_price = (By.XPATH, "//ul[@aria-labelledby='priceFacet']//span[text()='%s']")
    btn_color = (By.XPATH, "//button[@data-selected-facet-group-name='colorFacet']")
    cbx_color = (By.XPATH, "//ul[@aria-labelledby='colorFacet']//span[text()='%s']")
    txt_search_result = (By.XPATH, "//span[contains(text(),'items found')]")
    selected_filters = (By.XPATH, "//div[@id='products']/article/a")
 
    def search_data(self, text):
        self.find_and_send_keys(self.txt_search_field, text)
        self.find_and_click(self.search_loopa)

    def filter_data_by_brand_price_color(self, brand_name, price_range, color):
        try:
            self.find_and_click(self.btn_brand)
            self.find_and_click(self.remake_locator(self.chb_shop_by_brand, brand_name))
            self.hover_element(self.btn_price)
            self.find_and_click(self.btn_price)
            self.find_and_click(self.remake_locator(self.chb_price, price_range))
            self.hover_element(self.btn_color)
            self.find_and_click(self.btn_color)
            self.find_and_click(self.remake_locator(self.cbx_color, color))
        except Exception as e:
            logging.error(e)

    def check_selected_brand(self, brand_name):
        filters = self.find_all(self.selected_filters)
        for filter_item in filters:
            filter_text = filter_item.text
            if brand_name in filter_text:
                self.test_logger.info(f"Brand is included in {filter_text}")
                return True
            else:
                self.test_logger.error(f"Brand isn't included in {filter_text}")
                return False
         
    def check_selected_price(self, test_data_price):
        price_from_testdata = re.search(r'\$(\d+\.\d{2})', test_data_price)
        if price_from_testdata:
            extracted_price = float(price_from_testdata.group(1))
        filters = self.find_all(self.selected_filters)

        for filter_item in filters:
            filter_text = filter_item.text
            price_match = re.search(r'on sale for\s*\$(\d+\.\d{2})', filter_text, re.IGNORECASE)
            if price_match:
                price = float(price_match.group(1))
                if price <= extracted_price:
                    self.test_logger.info(f"{price} is correct.")
                    return True
                else:
                    self.test_logger.error(f"{filter_text} contain incorrect price - {price}.")
                    return False
            else:
                self.test_logger.error(f"No price found in: {filter_text}.")
                return False

    def get_result_count(self):
        return self.find(self.txt_search_result, get_text=True).split(" ")[0]
