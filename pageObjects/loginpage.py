from pageObjects.basepage import BasePage
from pageObjects.baseelements import *


class TxtEmail(BaseTxtElement):

    locator = (By.CSS_SELECTOR, "input#Email")


class TxtPassword(BaseTxtElement):

    locator = (By.CSS_SELECTOR, "input#Password")


class LoginButton(BaseButtonElement):

    locator = (By.CSS_SELECTOR, "input[type=submit]")


class ErrorMessage(BaseElement):

    locator = (By.CSS_SELECTOR, "div.message-error")


class LoginPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.txt_email = TxtEmail(driver)
        self.txt_password = TxtPassword(driver)
        self.loginbutton = LoginButton(driver)
        self.error_message = ErrorMessage(driver)

    def login(self, email, password):
        self.txt_email.enter(email)
        self.txt_password.enter(password)
        self.loginbutton.click()

    def enter_email(self, email):
        self.txt_email.enter(email)

    def enter_password(self, password):
        self.txt_password.enter(password)

    def click_login(self):
        self.loginbutton.click()

    def get_error_message(self):
        return self.error_message.text()

