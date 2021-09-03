from pageObjects.basepage import BasePage
from pageObjects.baseelements import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from testLib.lib import wait_till_dom_doesnot_change

class TxtEmail(BaseTxtElement):

    locator = (By.CSS_SELECTOR, "input#Email")


class TxtPassword(BaseTxtElement):

    locator = (By.CSS_SELECTOR, "input#Password")


class TxtFirstName(BaseTxtElement):

    locator = (By.CSS_SELECTOR, "input#FirstName")


class TxtLastName(BaseTxtElement):

    locator = (By.CSS_SELECTOR, "input#LastName")


class RadMale(BaseRadioElement):

    locator = (By.CSS_SELECTOR, "input#Gender_Male")


class RadFemale(BaseRadioElement):

    locator = (By.CSS_SELECTOR, "input#Gender_Female")


class TxtDOB(BaseTxtElement):

    locator = (By.CSS_SELECTOR, "input#DateOfBirth")


class TxtCompanyName(BaseTxtElement):

    locator = (By.CSS_SELECTOR, "input#Company")


class ChkTaxExempt(BaseCheckboxElement):

    locator = (By.CSS_SELECTOR, "input#IsTaxExempt")


class SelectNewsLetter(BaseElement):

    locator = (By.CSS_SELECTOR, "ul#SelectedNewsletterSubscriptionStoreIds_taglist + input")

    def select_store(self, storename):
        self.click()
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, f"//ul[@id='SelectedNewsletterSubscriptionStoreIds_listbox']/li[text()='{storename}']"))).click()

    def deselect_store(self, storename):
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, f"//ul[@id='SelectedNewsletterSubscriptionStoreIds_taglist']/li/span[text()='{storename}']/following-sibling::span"))).click()

    def get_all_available_options(self):
        elements = self.driver.find_elements_by_xpath("//ul[@id='SelectedNewsletterSubscriptionStoreIds_listbox']/li")
        return [e.get_attribute('innerHTML') for e in elements]

class SelectCustomerRoles(BaseElement):

    locator = (By.CSS_SELECTOR, "ul#SelectedCustomerRoleIds_taglist + input")

    def select_role(self, role):
        if not (role in self.get_selected_roles()):
            self.click()
            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
                (By.XPATH, f"//ul[@id='SelectedCustomerRoleIds_listbox']/li[text()='{role}']"))).click()

    def deselect_role(self, role):
        if role in self.get_selected_roles():
            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(
                (By.XPATH, f"//ul[@id='SelectedCustomerRoleIds_taglist']/li/span[text()='{role}']/following-sibling::span"))).click()

    def get_selected_roles(self):
        elements = self.driver.find_elements_by_xpath("//ul[@id='SelectedCustomerRoleIds_taglist']/li/span[text()]")
        return [e.text for e in elements]

    def deselect_all(self):
        for role in self.get_selected_roles():
            self.deselect_role(role)

    def get_all_available_roles(self):
        elements = self.driver.find_elements_by_xpath("//ul[@id='SelectedCustomerRoleIds_listbox']/li")
        return [e.get_attribute('innerHTML') for e in elements]

class LstVendorManager(BaseDropDownElement):

    locator = (By.CSS_SELECTOR, "select#VendorId")

    def get_managers_list(self):
        elements = self.all_options()
        return [e.text for e in elements]


class ChkActive(BaseCheckboxElement):

    locator = (By.CSS_SELECTOR, "input#Active")


class TxtAdminComment(BaseTxtElement):

    locator = (By.CSS_SELECTOR, "textarea#AdminComment")


class BtnSave(BaseButtonElement):

    locator = (By.CSS_SELECTOR, "button[name='save']")


class BtnSaveAndEdit(BaseButtonElement):

    locator = (By.CSS_SELECTOR, "button[name='save-continue']")


class AddCustomerPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.email = TxtEmail(driver)
        self.password = TxtPassword(driver)
        self.firstname = TxtFirstName(driver)
        self.lastname = TxtLastName(driver)
        self.male = RadMale(driver)
        self.female = RadFemale(driver)
        self.dob = TxtDOB(driver)
        self.taxexempt = ChkTaxExempt(driver)
        self.company_name = TxtCompanyName(driver)
        self.newsletter = SelectNewsLetter(driver)
        self.customer_roles = SelectCustomerRoles(driver)
        self.vendormanager = LstVendorManager(driver)
        self.active = ChkActive(driver)
        self.admincomment = TxtAdminComment(driver)
        self.save_btn = BtnSave(driver)
        self.saveandedit_btn = BtnSaveAndEdit(driver)

    def get_error_messages(self):
        elements = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'div.validation-summary-errors > ul > li')))

        return [element.text for element in elements]

    def get_alert_message(self):
        element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.alert')))

        return element.text[2:]

    def wait_till_page_is_loaded(self):
        wait_till_dom_doesnot_change(self.driver)

    def get_selected_roles(self):
        elements = self.driver.find_elements_by_xpath("//ul[@id='SelectedCustomerRoleIds_taglist']/li/span[text()]")
        return [e.text for e in elements]