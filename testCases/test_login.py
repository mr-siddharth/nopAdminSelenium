import pytest
from pageObjects.loginpage import LoginPage
import utilities.readconfig as config
from utilities.excelutils import *


class TestsLogIn:

    @pytest.fixture(scope="class")
    def credentials(self):
        return {
            "email": config.get_admin_email(),
            "password": config.get_admin_password()
        }

    @pytest.fixture
    def login_page(self, driver):
        self.base_url = config.get_base_url()
        self.driver = driver
        self.driver.get(self.base_url)
        return LoginPage(self.driver)

    @pytest.mark.sanity
    @pytest.mark.regression
    def test_login(self, logger, login_page, credentials):
        """Verifies that user is able to login with valid credentials."""

        logger.info(f"Attempting login using email: {credentials['email']} and password: {credentials['password']}")
        login_page.login(credentials['email'], credentials['password'])
        assert "dashboard" in login_page.get_title().lower()
        logger.info("login successful")

    @pytest.mark.parametrize("testdata", fetch_testdata("incorrect_credentials"))
    def test_incorrect_password(self, login_page, logger, testdata):
        """
        Verifies that user is NOT able to login with invalid credentials.
        Data is fetched from an excel file containing test data. Result of the
        test is written back to the same excel file. This excel file can be found
        in respective Test Run directory.
        """

        logger.info(f"Attempting login with email:{testdata['Email']} and password:{testdata['Password']}")
        try:
            login_page.login(testdata["Email"], testdata["Password"])
            assert "login" in login_page.get_title().lower()
        except Exception as e:
            write_test_results_failed("incorrect_credentials", testdata["rownum"], str(e))
            logger.exception(
                f"Test Case failed for useremail:{testdata['Email']} and password:{testdata['Password']}. "
                "Test DataRow no: " + str(testdata["rownum"]))
            pytest.fail()
        else:
            write_test_results_passed("incorrect_credentials", testdata["rownum"])
            logger.info("login failed as expected. "
                        "Test DataRow no: " + str(testdata["rownum"]))
