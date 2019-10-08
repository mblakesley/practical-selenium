import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from lib import common
from lib.web_element_plus import WebElementPlus


def get(ElementClass, locator_subs=None, wait=10):
    """
    Fetch first element described by ElementClass's attributes, waiting if it's not visible

    Args:
        ElementClass (class): any class with a Selenium locator tuple stored in the .locator attribute
        locator_subs (str OR list, optional): string or list of strings to substitute into
            the locator string using .format(). Defaults to None.
        wait (int, optional): max number of seconds to wait. Defaults to 10.

    Returns:
        Selenium element object: element object, with a few added convenience methods of our own
    """
    locator = _get_locator(ElementClass, locator_subs)
    elem = WebDriverWait(common.driver, wait).until(EC.visibility_of_element_located(locator))
    return WebElementPlus(elem)


def get_all(ElementClass, locator_subs=None, wait=10):
    """
    Fetch all visible elements described by ElementClass's attributes, waiting if none are visible

    Args:
        ElementClass (class): any class with a Selenium locator tuple stored in the .locator attribute
        locator_subs (str OR list, optional): string or list of strings to substitute into
            the locator string using .format(). Defaults to None.
        wait (int, optional): max number of seconds to wait. Defaults to 10.

    Returns:
        List of Selenium element objects: element objects, with a few added convenience methods of our own
    """
    locator = _get_locator(ElementClass, locator_subs)
    # TODO: this is supposed to find any, not all - make sure "any" works w/error msg in esswebpagenew
    elem_list = WebDriverWait(common.driver, wait).until(EC.visibility_of_any_elements_located(locator))
    return list(map(WebElementPlus, elem_list))


def click(ElementClass, locator_subs=None, wait=10):
    """
    Fetch first element described by ElementClass's attributes, waiting if it's not clickable

    Args:
        ElementClass (class): any class with a Selenium locator tuple stored in the .locator attribute
        locator_subs (str OR list, optional): string or list of strings to substitute into
            the locator string using .format(). Defaults to None.
        wait (int, optional): max number of seconds to wait. Defaults to 10.

    Returns:
        Selenium element object: element object, with a few added convenience methods of our own
    """
    locator = _get_locator(ElementClass, locator_subs)
    elem = WebDriverWait(common.driver, wait).until(EC.element_to_be_clickable(locator))
    elem.click()
    return WebElementPlus(elem)


def wait_until_stale(element, wait=10):
    """
    Wait until specified element is stale

    Args:
        element (WebElement/Plus object):
        wait (int, optional): max number of seconds to wait. Defaults to 10.
    """
    WebDriverWait(common.driver, wait).until(EC.staleness_of(element))


def _get_locator(ElementClass, locator_subs=None):
    """
    Fetch an element class's locator and, if provided, substitute into the locator string (2nd item) any <locator_subs>

    Args:
        ElementClass (class): any class with a Selenium locator tuple stored in the .locator attribute
        locator_subs (str OR list, optional): string or list of strings to substitute into
            the locator string using .format(). Defaults to None.

    Returns:
        tuple: Selenium locator tuple
    """
    locator = ElementClass.locator
    # TODO: locator substitution MVP, but not robust
    if locator_subs is not None:
        locator = (locator[0], locator[1].format(locator_subs))
    return locator


def wait(seconds):
    """
    Wait for the specified time. Wrapper for time.sleep()

    Args:
        seconds (int): number of seconds to wait
    """
    time.sleep(seconds)
