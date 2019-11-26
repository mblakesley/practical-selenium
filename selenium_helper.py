import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from web_element_wrapper import WebElementWrapper


driver = None


def find(selector, timeout=10):
    """
    Fetch first element matching selector and ensure it's visible.
    If no element matches this criteria, keep rechecking until one does or until timeout is reached.

    Args:
        selector (str OR tuple): either a CSS/XPath selector string OR a Selenium locator tuple
        timeout (int, optional): max number of seconds to wait. Defaults to 10.

    Returns:
        WebElementWrapper object: Selenium element object with added convenience methods
    """
    locator = locatorize(selector)
    elem = wait_until(EC.visibility_of_element_located(locator), timeout=timeout)
    return WebElementWrapper(elem)


def menu(selector, timeout=10):
    """
    Fetch first <select> element matching selector. If not visible, wait until it is or until timeout is reached.

    Args:
        selector (str OR tuple): either a CSS/XPath selector string OR a Selenium locator tuple
        timeout (int, optional): max number of seconds to wait. Defaults to 10.

    Returns:
        Select object: Selenium <select> element object
    """
    locator = locatorize(selector)
    elem = wait_until(EC.visibility_of_element_located(locator), timeout=timeout)
    return Select(elem)


def find_all(selector, timeout=10):
    """
    Fetch all visible elements matching selector.
    If none are visible, wait until at least 1 is or until timeout is reached.

    Args:
        selector (str OR tuple): either a CSS/XPath selector string OR a Selenium locator tuple
        timeout (int, optional): max number of seconds to wait. Defaults to 10.

    Returns:
        list of WebElementWrapper objects: list of Selenium element objects with added convenience methods
    """
    locator = locatorize(selector)
    elem_list = wait_until(EC.visibility_of_any_elements_located(locator), timeout=timeout)
    return list(map(WebElementWrapper, elem_list))


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
        seconds (int OR float): number of seconds to wait
    """
    time.sleep(seconds)


def wait_until(func, timeout=10, wait_between_calls=0.5):
    """
    Call specified function repeatedly until it returns a truthy value or until timeout is reached

    Args:
        func (function): Function to call repeatedly. This function MUST return truthy/falsy values, and
            MUST accept either 0 args or 1 arg: the driver. Selenium EC methods can be used here.
        timeout (int, optional): max number of seconds to wait. Defaults to 10.
        wait_between_calls (float, optional):
            if function returns a falsy value, how many seconds to wait before calling it again. Defaults to 0.5.
    """
    wait_obj = WebDriverWait(driver, timeout, poll_frequency=wait_between_calls)
    # .until() passes 1 arg (driver) to the function. So we try calling the function as is, and if we get a TypeError
    # (e.g. "TypeError: takes 0 args but 1 given"), we use a lambda to get the function to accept 1 arg
    try:
        return wait_obj.until(func)
    except TypeError:
        return wait_obj.until(lambda driver: func())


def wait_until_stale(element, timeout=10):
    """
    Wait until specified element is stale or timeout is reached

    Args:
        element (Selenium element object): target element
        timeout (int, optional): max number of seconds to wait. Defaults to 10.
    """
    wait_until(EC.staleness_of(element), timeout=timeout)
