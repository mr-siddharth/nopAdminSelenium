import pytest
from pageObjects.loginpage import LoginPage
import utilities.readconfig as config
from utilities.excelutils import *


class TestsLogIn:
    base_url = config.get_base_url()
    admin_email = config.get_admin_email()
    admin_password = config.get_admin_password()

    @pytest.fixture
    def launch_url(self, driver):
        self.driver = driver
        self.driver.get(self.base_url)

    @pytest.mark.sanity
    @pytest.mark.regression
    def test_login(self, logger, launch_url):
        """Verifies that user is able to login with valid credentials."""
        lp = LoginPage(self.driver)
        logger.info(f"Attempting login using email: {self.admin_email} and password: {self.admin_password}")
        lp.login(self.admin_email, self.admin_password)
        assert "dashboard" in lp.get_title().lower()
        logger.info("login successful")

    @pytest.mark.parametrize("testdata", fetch_testdata("incorrect_credentials"))
    def test_incorrect_password(self, launch_url, logger, testdata):
        """
        Verifies that user is NOT able to login with invalid credentials.
        Data is fetched from an excel file containing test data. Result of the
        test is written back to the same excel file. This excel file can be found
        in respective Test Run directory.
        """
        lp = LoginPage(self.driver)
        logger.info(f"Attempting login with email:{testdata['Email']} and password:{testdata['Password']}")
        try:
            lp.login(testdata["Email"], testdata["Password"])
            assert "login" in lp.get_title().lower()
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
