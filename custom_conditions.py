# Adds a few custom "expected conditions" on top of Selenium's
#
# These classes mimic Selenium's, but they take a pre-found element instead of a locator.
# That's helpful for us because of the "division of labor" in our helper functions & classes,
# which prevents our element objects from knowing how they were located.


class element_to_be_clickable:
    """An implementation of Selenium's "element_to_be_clickable" for when the element is already found"""
    def __init__(self, element):
        self.element = element

    def __call__(self, _):
        return self.element.is_displayed() and self.element.is_enabled()
