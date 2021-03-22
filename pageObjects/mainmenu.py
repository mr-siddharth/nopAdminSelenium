from pageObjects.basepage import BasePage
from pageObjects.baseelements import *


class LnkCustomers(BaseElement):

    locator = (By.XPATH, "//a[@class='nav-link']/p[text()=' Customers']/parent::a")


class SecCustomers(BaseElement):

    locator = (By.XPATH, "//*[contains(@class,'treeview')]/a/p[contains(text(),'Customers')]/parent::a")


class MainMenu(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.customers_lnk = LnkCustomers(driver)
        self.customers_section = SecCustomers(driver)

