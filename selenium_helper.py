import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from web_element_plus import WebElementPlus


driver = None


def find(selector, timeout=10):
    """
    Fetch first element matching selector. If it's not visible, wait until it is or until timeout is reached.

    Args:
        selector (str OR tuple): either a CSS/XPath selector string OR a Selenium locator tuple
        timeout (int, optional): max number of seconds to wait. Defaults to 10.

    Returns:
        WebElementPlus object: Selenium element object, with a few added convenience methods
    """
    locator = locatorize(selector)
    elem = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))
    return WebElementPlus(elem)


def menu(selector, timeout=10):
    """
    Fetch first <select> element matching selector. If not visible, wait until it is or until timeout is reached.

    Args:
        selector (str OR tuple): either a CSS/XPath selector string OR a Selenium locator tuple
        timeout (int, optional): max number of seconds to wait. Defaults to 10.

    Returns:
        Select object: Selenium <select> element object, with a few added convenience methods
    """
    locator = locatorize(selector)
    elem = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))
    return Select(elem)


def find_all(selector, timeout=10):
    """
    Fetch all visible elements matching selector.
    If none are visible, wait until at least 1 is or until timeout is reached.

    Args:
        selector (str OR tuple): either a CSS/XPath selector string OR a Selenium locator tuple
        timeout (int, optional): max number of seconds to wait. Defaults to 10.

    Returns:
        list of WebElementPlus objects: list of Selenium element objects, with a few added convenience methods
    """
    locator = locatorize(selector)
    elem_list = WebDriverWait(driver, timeout).until(EC.visibility_of_any_elements_located(locator))
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


def wait_until_stale(element, timeout=10):
    """
    Wait until specified element is stale or timeout is reached

    Args:
        element (Selenium element object): target element
        timeout (int, optional): max number of seconds to wait. Defaults to 10.
    """
    WebDriverWait(driver, timeout).until(EC.staleness_of(element))
