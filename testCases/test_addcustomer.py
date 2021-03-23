import pytest
from pageObjects.loginpage import LoginPage
from pageObjects.addcustomerpage import AddCustomerPage
from pageObjects.mainmenu import MainMenu
from pageObjects.customerspage import CustomersPage
import utilities.readconfig as config
from utilities.excelutils import *
from testLib.lib import *

@pytest.mark.regression
class TestsAddNewCustomer:
    base_url = config.get_base_url()
    admin_email = config.get_admin_email()
    admin_password = config.get_admin_password()

    @pytest.fixture
    def setup(self, driver, logger):
        self.driver = driver
        self.driver.get(self.base_url)
        lp = LoginPage(self.driver)
        logger.warning("Attempting login")
        lp.login(self.admin_email, self.admin_password)
        assert "dashboard" in lp.get_title().lower()
        logger.info("login successful")
        wait_till_dom_doesnot_change(self.driver)
        mm = MainMenu(self.driver)
        mm.customers_section.click()
        mm.customers_lnk.click()
        CustomersPage(self.driver).wait_till_page_is_loaded(duration=2)
        CustomersPage(self.driver).btn_addnew.click()
        AddCustomerPage(self.driver).wait_till_page_is_loaded()

    @pytest.mark.sanity
    def test_add_customer(self, setup):
        add_cust_page = AddCustomerPage(self.driver)
        add_cust_page.email.enter(get_random_string() + "@gmail.com")
        add_cust_page.password.enter("password123")
        add_cust_page.firstname.enter("Chicky")
        add_cust_page.lastname.enter("Sharma")
        add_cust_page.male.click()
        add_cust_page.dob.enter("9/3/1985")
        add_cust_page.company_name.enter("SuperSaber Inc.")
        add_cust_page.taxexempt.select()
        add_cust_page.newsletter.select_store("Your store name")
        add_cust_page.customer_roles.select_role("Registered")
        add_cust_page.customer_roles.select_role("Forum Moderators")
        add_cust_page.vendormanager.select_by_visible_text("Vendor 1")
        add_cust_page.admincomment.enter("Testing 1 2 3")
        add_cust_page.save_btn.click()
        assert add_cust_page.get_alert_message() == "The new customer has been added successfully."

    def test_errormessage_noemail_registered_customer(self, setup):
        add_cust_page = AddCustomerPage(self.driver)
        add_cust_page.customer_roles.select_role("Registered")
        add_cust_page.save_btn.click()
        error_messages_actual = add_cust_page.get_error_messages()
        error_messages_expected = ["'Email' must not be empty.",
                                   "Valid Email is required for customer to be in 'Registered' role"]

        assert error_messages_actual.sort() == error_messages_expected.sort()

    def test_alertmessage_noemail_registered_customer(self, setup):
        add_cust_page = AddCustomerPage(self.driver)
        add_cust_page.customer_roles.select_role("Registered")
        add_cust_page.save_btn.click()
        assert add_cust_page.get_alert_message() == "Valid Email is required for customer to be in 'Registered' role"

    def test_errormessage_role_cannot_be_both_registered_and_guests(self, setup):
        add_cust_page = AddCustomerPage(self.driver)
        add_cust_page.email.enter(get_random_string() + "@gmail.com")
        add_cust_page.customer_roles.select_role("Registered")
        add_cust_page.customer_roles.select_role("Guests")
        add_cust_page.save_btn.click()
        assert add_cust_page.get_error_messages() == \
            ["The customer cannot be in both 'Guests' and 'Registered' customer roles"]

    def test_alertmessage_role_cannot_be_both_registered_and_guests(self, setup):
        add_cust_page = AddCustomerPage(self.driver)
        add_cust_page.email.enter(get_random_string() + "@gmail.com")
        add_cust_page.customer_roles.select_role("Registered")
        add_cust_page.customer_roles.select_role("Guests")
        add_cust_page.save_btn.click()
        error_messages_actual = add_cust_page.get_error_messages()
        assert add_cust_page.get_alert_message() == "The customer cannot be in both 'Guests' and 'Registered' customer roles"


class TestDropDownLists:
    base_url = config.get_base_url()
    admin_email = config.get_admin_email()
    admin_password = config.get_admin_password()

    @pytest.fixture(scope="class")
    def setup(self, request, driver_class_scoped, logger):
        self.driver = driver_class_scoped
        request.cls.driver = driver_class_scoped
        self.driver.get(self.base_url)
        lp = LoginPage(self.driver)
        logger.warning("Attempting login")
        lp.login(self.admin_email, self.admin_password)
        assert "dashboard" in lp.get_title().lower()
        logger.info("login successful")
        wait_till_dom_doesnot_change(self.driver, 2)
        mm = MainMenu(self.driver)
        mm.customers_section.click()
        mm.customers_lnk.click()
        CustomersPage(self.driver).wait_till_page_is_loaded(duration=2)
        CustomersPage(self.driver).btn_addnew.click()
        AddCustomerPage(self.driver).wait_till_page_is_loaded()

    @pytest.mark.regression
    @pytest.mark.sanity
    def test_customer_roles_dropdown(self, setup):
        add_cust_page = AddCustomerPage(self.driver)
        roles_list_actual = add_cust_page.customer_roles.get_all_available_roles()
        roles_list_expected = ["Administrators", "Forum Moderators", "Guests", "Registered", "Vendors"]
        roles_list_actual.sort()
        roles_list_expected.sort()
        assert roles_list_actual == roles_list_expected

    @pytest.mark.regression
    def test_newsletter_dropdown(self, setup):
        add_cust_page = AddCustomerPage(self.driver)
        newsletter_list_actual = add_cust_page.newsletter.get_all_available_options()
        newsletter_list_expected = ["Your store name", "Test store 2"]
        newsletter_list_actual.sort()
        newsletter_list_expected.sort()
        assert newsletter_list_actual == newsletter_list_expected

    @pytest.mark.sanity
    def test_vendor_manager_dropdown(self, setup):
        add_cust_page = AddCustomerPage(self.driver)
        manager_list_actual = add_cust_page.vendormanager.get_managers_list()
        manager_list_expected = ['Not a vendor', 'Vendor 1', 'Vendor 2']
        assert manager_list_actual == manager_list_expected
