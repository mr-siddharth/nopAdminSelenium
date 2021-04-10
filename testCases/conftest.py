import pytest
from selenium import webdriver
from utilities.logger import get_logger
from testLib.lib import *
from configurations import testconfig
import os, shutil
import traceback

firefox_driver_path = "C:\\Users\\Siddharth\\Google Drive\\PycharmProjects\\MyHome\\seleniumdrivers\\geckodriver.exe"
chrome_driver_path = "C:\\Users\\Siddharth\\Google Drive\\PycharmProjects\\MyHome\\seleniumdrivers\\chromedriver.exe"

# ---------Initial Folder & File Setup---------- #
testconfig.TEST_RUN_DIR = ".\\TestRuns\\" + re.sub(":", ".", "Test Run - " + str(datetime.now())) + "\\"
testconfig.LOG_DIR = testconfig.TEST_RUN_DIR + "\\logs\\"
testconfig.SCREENSHOTS_DIR = testconfig.TEST_RUN_DIR + "\\screenshots\\"
os.makedirs(testconfig.TEST_RUN_DIR)
os.makedirs(testconfig.LOG_DIR)
os.makedirs(testconfig.SCREENSHOTS_DIR)
print("Find test run artifacts at: " + os.getcwd() + testconfig.TEST_RUN_DIR[1:])
# ---------------------------------------------- #


# -- set up a hook to be able to check if a test has failed --
# the attribute set up by this hook for the item (test function) will be used
# to track whether the test case failed or passed. If the test case fails, a
# screen-shot will automatically be taken using the same driver instance before
# the driver is closed.
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the result object
    outcome = yield
    res = outcome.get_result()

    # set a result attribute to the item (test function) for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, res.when + "_result", res)

    if res.when == "call" and res.failed:
        get_logger().exception(f"Test case --> {item.nodeid} failed. Error Message:\n {traceback.format_exc()}")
    elif res.when == 'setup' and res.failed:
        get_logger().exception(f"Setup for {item.nodeid} failed. Error Message:\n {traceback.format_exc()}")


# Adding a custom command line option
def pytest_addoption(parser):
    parser.addoption("--browser", default="firefox", help="The browser you want to run your tests in. "
                                                          "Default is firefox.")

# Fixture that returns the value of the command line option
@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture
def driver(browser, request, logger):
    if browser.lower() == "chrome":
        driver = webdriver.Chrome(executable_path=chrome_driver_path)
    elif browser.lower() == "firefox":
        driver = webdriver.Firefox(executable_path=firefox_driver_path)
    elif browser.lower() == "grid":
        selenium_grid_url = "http://192.168.80.97:4444/wd/hub"
        driver = webdriver.Remote(command_executor=selenium_grid_url, desired_capabilities=webdriver.DesiredCapabilities.CHROME.copy())
    else:
        pytest.exit("Unknown browser specified", 1)

    driver.maximize_window()

    yield driver

    # Determine if the test case failed using the attribute set up by the
    # pytest_runtest_makereport hook. Take a screenshot if the test case
    # failed before the driver instance is closed
    try:
        if request.node.setup_result.failed:
            print("setting up a test failed!", request.node.nodeid)
            take_screenshot(driver, "FAILED_" + request.node.name)
        elif request.node.setup_result.passed:
            if request.node.call_result.failed:
                take_screenshot(driver, "FAILED_" + request.node.name)
    except Exception:
        print(request.node.nodeid + ": An exception occurred while taking a screenshot. Error Message:\n" + traceback.format_exc())
        logger.exception(request.node.nodeid + ": An exception occurred while taking a screenshot. Error Message:\n" + traceback.format_exc())
    finally:
        driver.quit()


@pytest.fixture(scope="class")
def driver_class_scoped(browser, request, logger):
    if browser.lower() == "chrome":
        driver = webdriver.Chrome(executable_path=chrome_driver_path)
    elif browser.lower() == "firefox":
        driver = webdriver.Firefox(executable_path=firefox_driver_path)
    elif browser.lower() == "grid":
        selenium_grid_url = "http://localhost:4444/wd/hub"
        driver = webdriver.Remote(command_executor=selenium_grid_url, desired_capabilities=webdriver.DesiredCapabilities.CHROME.copy())
    else:
        pytest.exit("Unknown browser specified", 1)

    driver.maximize_window()

    yield driver

    # Determine if any of the test case belonging to the class failed using the attribute set up by the
    # pytest_runtest_makereport hook. Take a screenshot if any test case
    # failed before the driver instance is closed
    try:
        all_test_functions = [item for item in request.session.items if item.parent.nodeid == request.node.nodeid]
        if all_test_functions != []:
            if all_test_functions[0].setup_result.failed:  # i.e. attribute could not be setup because class setup failed
                print("setting up the test class failed!", request.node.nodeid)
                take_screenshot(driver, "FAILED_" + request.keywords.node.name)
            elif False in [test.call_result.passed for test in all_test_functions]:  # i.e. one of the test cases in the class failed
                take_screenshot(driver, "FAILED_" + request.keywords.node.name)
    except:
        print(request.node.nodeid + ": An exception occurred while taking a screenshot")
        logger.exception(request.node.nodeid + ": An exception occurred while taking a screenshot")
    finally:
        driver.quit()


@pytest.fixture(scope="session")
def logger():
    return get_logger()


##################### For HTML Report ##############################
def pytest_configure(config):
    config._metadata['Project Name'] = 'nop Commerce Admin App'
    config._metadata['Module Name'] = 'Customers'
    config._metadata['Tester'] = 'Siddharth'

def pytest_metadata(metadata):
    # Removing the following fields for the report
    metadata.pop('PLATFORM', None)
    metadata.pop('Packages', None)

####################################################################
