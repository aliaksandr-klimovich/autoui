from selenium.webdriver.remote.webelement import WebElement


class Input(WebElement):
    def type(self, text):
        self.clear()
        self.send_keys(text)


class Button(WebElement):
    pass
