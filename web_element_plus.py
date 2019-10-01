from selenium.webdriver.remote.webelement import WebElement


class WebElementPlus(WebElement):
    """TODO"""
    def __init__(self, sel_element):
        """TODO"""
        super().__init__(sel_element._parent, sel_element._id, sel_element._w3c)

    def replace(self, *value):
        """TODO"""
        self.clear()
        self.send_keys(*value)
