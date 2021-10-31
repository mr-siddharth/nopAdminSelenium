from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class BaseElement:
    """
    Base class for all the other types of web elements.
    Requires locator variable to be set by a sub-class
    """

    def __init__(self, driver):
        self.driver = driver

    def text(self):
        return WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(self.locator)).text

    def click(self):
        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(self.locator)).click()


class BaseTxtElement(BaseElement):
    """
    Class for web element, <input type='text'>.
    Requires locator variable to be set by a sub-class
    """

    def enter(self, value):
        textbox = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(self.locator))
        textbox.clear()
        textbox.send_keys(value)

    def value(self):
        return WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(self.locator))\
            .get_attribute("value")


class BaseButtonElement(BaseElement):
    """
    Class for web element, <input type='button'> or <button>
    Requires locator variable to be set by a sub-class
    """
    pass


class BaseRadioElement(BaseElement):
    """
    Class for web element, <input type='radio'>.
    Requires locator variable to be set by a sub-class
    """

    def click(self):
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(self.locator)).click()

    def is_selected(self):
        return WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(self.locator)).is_selected()


class BaseCheckboxElement(BaseElement):
    """
    Class for web element, <input type='checkbox'>.
    Requires locator variable to be set by a sub-class
    """
    def is_selected(self):
        return WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(self.locator)).is_selected()

    def select(self):
        if not self.is_selected():
            self.click()

    def deselect(self):
        if self.is_selected():
            self.click()


class BaseDropDownElement(BaseElement):
    """
    Class for web element, <select>.
    Requires locator variable to be set by a sub-class
    """

    def select_by_visible_text(self, text):
        Select(WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.locator))).select_by_visible_text(text)

    def select_by_index(self, index):
        Select(WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.locator))).select_by_index(index)

    def select_by_value(self, value):
        Select(WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(self.locator))).select_by_value(value)

    def selected_option(self):
        """The currently selected option in a normal select"""
        return Select(WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(self.locator))).first_selected_option

    def all_options(self):
        """Returns a list of all options belonging to this select tag"""
        return Select(WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(self.locator))).options