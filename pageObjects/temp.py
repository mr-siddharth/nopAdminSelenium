from time import sleep
from selenium import webdriver
from loginpage import LoginPage
from addcustomerpage import AddCustomerPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from testLib.lib import wait_till_dom_doesnot_change

driver = webdriver.Firefox(
    executable_path="C:\\Users\\Siddharth\\Google Drive\\PycharmProjects\\MyHome\\seleniumdrivers\\geckodriver.exe")
driver.get("https://admin-demo.nopcommerce.com/")
# textbox = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#Email")))
# textbox.clear()
# textbox.send_keys("Adfadsfadfasd")
loginpage = LoginPage(driver)
loginpage.login("admin@yourstore.com", "admin")
driver.get("https://admin-demo.nopcommerce.com/Admin/Customer/Create")
wait_till_dom_doesnot_change(driver)

acp = AddCustomerPage(driver)
acp.customerrole.select_role("Forum Moderators")
print(acp.get_selected_roles())
acp.customerrole.select_role("Guests")
acp.customerrole.deselect_role("Forum Moderators")
print(acp.get_selected_roles())
acp.customerrole.deselect_all()
print(acp.get_selected_roles())
# message = acp.get_alert_message()
# print(acp.get_error_messages())


driver.close()

# import logging
#
# logging.basicConfig(format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
#
# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')