import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from web_element_wrapper import WebElementWrapper


class ChromeWrapper(Chrome):
    def find(self, selector, timeout=10):
        """
        Fetch first element matching selector and ensure it's visible.
        If no elements match this criteria, recheck until one does or until timeout is reached.

        Args:
            selector (str OR tuple): either a CSS/XPath selector string OR a Selenium locator tuple
            timeout (int, optional): max number of seconds to wait. Defaults to 10.

        Returns:
            WebElementWrapper object: Selenium element object with added convenience methods
        """
        locator = self.locatorize(selector)
        elem = self.wait_until(EC.visibility_of_element_located(locator), timeout=timeout)
        return WebElementWrapper(elem)

    def find_all(self, selector, timeout=10):
        """
        Fetch all visible elements matching selector.
        If none match this criteria, recheck until at least one does or until timeout is reached.

        Args:
            selector (str OR tuple): either a CSS/XPath selector string OR a Selenium locator tuple
            timeout (int, optional): max number of seconds to wait. Defaults to 10.

        Returns:
            list of WebElementWrapper objects: list of Selenium element objects with added convenience methods
        """
        locator = self.locatorize(selector)
        elem_list = self.wait_until(EC.visibility_of_any_elements_located(locator), timeout=timeout)
        return list(map(WebElementWrapper, elem_list))

    def find_menu(self, selector, timeout=10):
        """
        Fetch first <select> element matching selector and ensure it's visible.
        If no elements match this criteria, recheck until one does or until timeout is reached.

        Args:
            selector (str OR tuple): either a CSS/XPath selector string OR a Selenium locator tuple
            timeout (int, optional): max number of seconds to wait. Defaults to 10.

        Returns:
            Select object: Selenium <select> element object
        """
        locator = self.locatorize(selector)
        elem = self.wait_until(EC.visibility_of_element_located(locator), timeout=timeout)
        return Select(elem)

    def find_by_text(self, basic_selector, text, matching_strategy='contains', timeout=10):
        """
        Fetch first element matching selector and containing the specified text and ensure it's visible.
        If no elements match this criteria, recheck until one does or until timeout is reached.

        Note: This method won't work when text is split across parent/child DOM elements, e.g.:
            given: <a><span>some text</span></a>, then: find_by_text('a', 'some text') will work
            given: <a>some<span>text</span></a>, then: find_by_text('a', 'some text') WON'T work

        Args:
            basic_selector (str): simple selector string for 1 element type, e.g. 'a' or 'tr'. Anything fancier WON'T work
            text (str): text to look for
            matching_strategy ({'contains', 'starts-with'}, optional):
                matching strategy to use on the text check. Defaults to 'contains'.
            timeout (int, optional): max number of seconds to wait. Defaults to 10.

        Returns:
            WebElementWrapper object: Selenium element object with added convenience methods
        """
        # This full selector finds any element with the given text,
        # then looks for the closest "ancestor or self" element matching <basic_selector>
        full_selector = '//*[{}(text(),"{}")]/ancestor-or-self::{}[1]'.format(
            matching_strategy, text, basic_selector)
        return self.find(full_selector, timeout=timeout)

    @staticmethod
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
        # here we guess that if the selector starts with a '/' or './', it's xpath, not CSS
        elif selector.startswith('/') or selector.startswith('./'):
            return (By.XPATH, selector)
        else:
            return (By.CSS_SELECTOR, selector)

    @staticmethod
    def wait(seconds):
        """
        Wait for the specified time.

        Args:
            seconds (int OR float): number of seconds to wait
        """
        time.sleep(seconds)

    def wait_until(self, func, timeout=10, wait_between_calls=0.5):
        """
        Call specified function repeatedly until it returns a truthy value or until timeout is reached

        Args:
            func (function): Function to call repeatedly. This function MUST return truthy/falsy values, and
                MUST accept either 0 args or 1 arg: the driver. Selenium EC methods can be used here.
            timeout (int, optional): max number of seconds to wait. Defaults to 10.
            wait_between_calls (float, optional):
                if function returns a falsy value, how many seconds to wait before calling it again. Defaults to 0.5.
        """
        wait_obj = WebDriverWait(self, timeout, poll_frequency=wait_between_calls)
        # .until() passes 1 arg (driver) to the function. So we try calling the function as is, & if we get a TypeError
        # (e.g. "TypeError: takes 0 args but 1 given"), we use a lambda to get the function to accept 1 arg
        try:
            return wait_obj.until(func)
        except TypeError:
            return wait_obj.until(lambda driver: func())

    def wait_until_stale(self, element, timeout=10):
        """
        Wait until specified element is stale or timeout is reached

        Args:
            element (Selenium element object): target element
            timeout (int, optional): max number of seconds to wait. Defaults to 10.
        """
        self.wait_until(EC.staleness_of(element), timeout=timeout)
