import pytest
from pageObjects.loginpage import LoginPage
from pageObjects.addcustomerpage import AddCustomerPage
from pageObjects.mainmenu import MainMenu
from pageObjects.customerspage import CustomersPage
import utilities.readconfig as config
from testLib.lib import *


@pytest.fixture(scope="module")
def credentials():
    return {
        "email": config.get_admin_email(),
        "password": config.get_admin_password()
    }


@pytest.fixture
def add_customer_page(driver, logger, credentials):
    base_url = config.get_base_url()
    driver.get(base_url)

    lp = LoginPage(driver)
    logger.info(f"Attempting login using email: {credentials['email']} and "
                f"password: {credentials['password']}")
    lp.login(credentials['email'], credentials['password'])
    assert "dashboard" in lp.get_title().lower()
    logger.info("login successful")
    wait_till_dom_doesnot_change(driver)

    mm = MainMenu(driver)
    mm.customers_section.click()
    mm.customers_lnk.click()

    cp = CustomersPage(driver)
    cp.wait_till_page_is_loaded(duration=2)
    cp.btn_addnew.click()

    add_cust_page = AddCustomerPage(driver)
    add_cust_page.wait_till_page_is_loaded()
    return add_cust_page


@pytest.mark.regression
@pytest.mark.usefixtures("credentials", "add_customer_page")
class TestsAddNewCustomer:

    @pytest.mark.sanity
    def test_add_customer(self, add_customer_page):
        add_customer_page.email.enter(get_random_string() + "@gmail.com")
        add_customer_page.password.enter("password123")
        add_customer_page.firstname.enter("Aman")
        add_customer_page.lastname.enter("Sharma")
        add_customer_page.male.click()
        add_customer_page.dob.enter("9/3/1985")
        add_customer_page.company_name.enter("SuperSaber Inc.")
        add_customer_page.taxexempt.select()
        add_customer_page.newsletter.select_store("Your store name")
        add_customer_page.customer_roles.select_role("Registered")
        add_customer_page.customer_roles.select_role("Forum Moderators")
        add_customer_page.vendormanager.select_by_visible_text("Vendor 1")
        add_customer_page.admincomment.enter("Testing 1 2 3")
        add_customer_page.save_btn.click()
        assert add_customer_page.get_alert_message() == "The new customer has been added successfully."

    def test_errormessage_noemail_registered_customer(self, add_customer_page):
        add_customer_page.customer_roles.select_role("Registered")
        add_customer_page.save_btn.click()
        error_messages_actual = add_customer_page.get_error_messages()
        error_messages_expected = ["'Email' must not be empty.",
                                   "Valid Email is required for customer to be in 'Registered' role"]

        assert error_messages_actual.sort() == error_messages_expected.sort()

    def test_alertmessage_noemail_registered_customer(self, add_customer_page):
        add_customer_page.customer_roles.select_role("Registered")
        add_customer_page.save_btn.click()
        assert add_customer_page.get_alert_message() == "Valid Email is required for customer to be in 'Registered' role"

    def test_errormessage_role_cannot_be_both_registered_and_guests(self, add_customer_page):
        add_customer_page.email.enter(get_random_string() + "@gmail.com")
        add_customer_page.customer_roles.select_role("Registered")
        add_customer_page.customer_roles.select_role("Guests")
        add_customer_page.save_btn.click()
        assert add_customer_page.get_error_messages() == \
               ["The customer cannot be in both 'Guests' and 'Registered' customer roles"]

    def test_alertmessage_role_cannot_be_both_registered_and_guests(self, add_customer_page):
        add_customer_page.email.enter(get_random_string() + "@gmail.com")
        add_customer_page.customer_roles.select_role("Registered")
        add_customer_page.customer_roles.select_role("Guests")
        add_customer_page.save_btn.click()
        assert add_customer_page.get_alert_message() == "The customer cannot be in both 'Guests' and 'Registered' customer roles"


@pytest.mark.usefixtures("credentials")
class TestDropDownLists:

    @pytest.fixture(scope="class")
    def add_customer_page(self, driver_class_scoped, logger, credentials, request):
        driver = driver_class_scoped
        base_url = config.get_base_url()
        request.cls.base_url = base_url
        request.cls.driver = driver
        driver.get(base_url)

        lp = LoginPage(driver)
        logger.info(f"Attempting login using email: {credentials['email']} and "
                    f"password: {credentials['password']}")
        lp.login(credentials['email'], credentials['password'])
        assert "dashboard" in lp.get_title().lower()
        logger.info("login successful")
        wait_till_dom_doesnot_change(driver)

        mm = MainMenu(driver)
        mm.customers_section.click()
        mm.customers_lnk.click()

        cp = CustomersPage(driver)
        cp.wait_till_page_is_loaded(duration=2)
        cp.btn_addnew.click()

        add_cust_page = AddCustomerPage(driver)
        add_cust_page.wait_till_page_is_loaded()
        return add_cust_page

    @pytest.mark.regression
    @pytest.mark.sanity
    def test_customer_roles_dropdown(self, add_customer_page):
        roles_list_actual = add_customer_page.customer_roles.get_all_available_roles()
        roles_list_expected = ["Administrators", "Forum Moderators", "Guests", "Registered", "Vendors"]
        roles_list_actual.sort()
        roles_list_expected.sort()
        assert roles_list_actual == roles_list_expected

    @pytest.mark.regression
    def test_newsletter_dropdown(self, add_customer_page):
        newsletter_list_actual = add_customer_page.newsletter.get_all_available_options()
        newsletter_list_expected = ["Your store name", "Test store 2"]
        newsletter_list_actual.sort()
        newsletter_list_expected.sort()
        assert newsletter_list_actual == newsletter_list_expected

    @pytest.mark.sanity
    def test_vendor_manager_dropdown(self, add_customer_page):
        manager_list_actual = add_customer_page.vendormanager.get_managers_list()
        manager_list_expected = ['Not a vendor', 'Vendor 1', 'Vendor 2']
        assert manager_list_actual == manager_list_expected
