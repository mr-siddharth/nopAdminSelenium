from pageObjects.basepage import BasePage
from pageObjects.baseelements import *
from testLib.lib import wait_till_dom_doesnot_change


class BtnAddNew(BaseElement):
    locator = (By.XPATH, "//a[normalize-space() = 'Add new']")


class CustomersPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.btn_addnew = BtnAddNew(driver)

    def wait_till_page_is_loaded(self, duration=3, poll_frequency=0.5):
        wait_till_dom_doesnot_change(self.driver, duration, poll_frequency)
