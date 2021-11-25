from datetime import datetime
import re
from time import sleep, time
from configurations import testconfig
import random
import string
import os


def take_screenshot(driver, filetitle="scr"):
    driver.save_screenshot(os.path.join(
        testconfig.SCREENSHOTS_DIR, re.sub(":", ".", filetitle + " - " + str(datetime.now()) + ".png")))


def take_screenshot_fullpage(driver, filetitle="scr"):
    """Doesn't work with chrome."""
    old_size = driver.get_window_size()
    old_width, old_height = old_size['width'], old_size['height']
    height = driver.execute_script("return document.body.scrollHeight")  # + \
    # driver.execute_script("return document.querySelector('footer').scrollHeight")
    width = driver.execute_script("return document.body.scrollWidth")
    print(height, width)
    driver.set_window_size(width, height)
    driver.save_screenshot(os.path.join(
        testconfig.SCREENSHOTS_DIR, re.sub(":", ".", filetitle + " - " + str(datetime.now()) + ".png")))

    # Restore Old Window Size:
    driver.set_window_size(old_width, old_height)


def wait_till_dom_doesnot_change(driver, duration=3, poll_frequency=0.5):
    """Waits till the rendered DOM doesn't change for the given duration"""
    dom1 = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
    start = time()
    while time() - start < duration:
        sleep(poll_frequency)
        dom2 = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
        if not (dom2 == dom1):
            start = time()  # reset the start time as the page source changed
            dom1 = dom2


def get_random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
