import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


import common
from web_element_plus import WebElementPlus


def get(selector, wait=10):
    """
    Fetch first element matching selector, waiting if it's not visible

    Args:
        selector (str OR tuple): either a CSS/XPath selector string OR a Selenium locator tuple
        wait (int, optional): max number of seconds to wait. Defaults to 10.

    Returns:
        WebElementPlus object: Selenium element object, with a few added convenience methods
    """
    locator = locatorize(selector)
    elem = WebDriverWait(common.driver, wait).until(EC.visibility_of_element_located(locator))
    return WebElementPlus(elem)


def get_all(selector, wait=10):
    """
    Fetch all visible elements matching selector, waiting only if none are visible

    Args:
        selector (str OR tuple): either a CSS/XPath selector string OR a Selenium locator tuple
        wait (int, optional): max number of seconds to wait. Defaults to 10.

    Returns:
        list of WebElementPlus objects: list of Selenium element objects, with a few added convenience methods
    """
    locator = locatorize(selector)
    elem_list = WebDriverWait(common.driver, wait).until(EC.visibility_of_any_elements_located(locator))
    return list(map(WebElementPlus, elem_list))


def locatorize(selector):
    """
    Convert <selector> to a Selenium locator, if it isn't one already.

    Args:
        selector (str OR tuple): either a CSS/XPath selector string OR a Selenium locator tuple

    Returns:
        tuple: Selenium locator tuple
    """
    if isinstance(selector, (tuple, list)):
        return selector
    # here we guess that if the selector starts with a '/', it's xpath, not CSS
    elif selector.startswith('/'):
        return (By.XPATH, selector)
    else:
        return (By.CSS_SELECTOR, selector)


def wait(seconds):
    """
    Wait for the specified time.

    Args:
        seconds (int): number of seconds to wait
    """
    time.sleep(seconds)


def wait_until_stale(element, wait=10):
    """
    Wait until specified element is stale

    Args:
        element (Selenium element object): target element
        wait (int, optional): max number of seconds to wait. Defaults to 10.
    """
    WebDriverWait(common.driver, wait).until(EC.staleness_of(element))
