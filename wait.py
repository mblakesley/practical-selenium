from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from lib import common
from lib.web_element_plus import WebElementPlus


def find(ElemClass, locator_subs=None, wait=10):
    """TODO"""
    locator = _get_locator(ElemClass, locator_subs)
    elem = WebDriverWait(common.driver, wait).until(EC.presence_of_element_located(locator))
    return WebElementPlus(elem)


def find_all(ElemClass, locator_subs=None, wait=10):
    """TODO"""
    locator = _get_locator(ElemClass, locator_subs)
    elem_list = WebDriverWait(common.driver, wait).until(EC.presence_of_all_elements_located(locator))
    return list(map(WebElementPlus, elem_list))


def visible(ElemClass, locator_subs=None, wait=10):
    """TODO"""
    locator = _get_locator(ElemClass, locator_subs)
    elem = WebDriverWait(common.driver, wait).until(EC.visibility_of_element_located(locator))
    return WebElementPlus(elem)


def click(ElemClass, locator_subs=None, wait=10):
    """TODO"""
    locator = _get_locator(ElemClass, locator_subs)
    elem = WebDriverWait(common.driver, wait).until(EC.element_to_be_clickable(locator))
    elem.click()
    return WebElementPlus(elem)


def stale(element, wait=10):
    """TODO"""
    WebDriverWait(common.driver, wait).until(EC.staleness_of(element))


def _get_locator(ElemClass, locator_subs=None):
    locator = ElemClass.locator
    # TODO: locator subs MVP, but not robust
    if locator_subs is not None:
        locator = (locator[0], locator[1].format(locator_subs))
    return locator
