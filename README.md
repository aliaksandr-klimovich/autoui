# autoui
Web site automation testing framework.

Status: :umbrella:

The goal is to show how to implement custom page object pattern in python. 
This project was inspired by `webium` project and structural patterns in java.
It is not designed for production usage. It's only my own approach to test web sites.

Author: Alex Klimovich

## Requirements
- python 2.7.10
- selenium 2.48.0
- nose 1.3.7 (for internal tests)
- mock 1.3.0 (for internal tests)

## Usage

### Basic test

```python
from autoui.base import BasePage
from autoui.elements.common import Button, Input
from autoui.locators import XPath, ID


class YaPage(BasePage):
    url = 'http://ya.ru'
    input = Input(ID('text'))
    find = Button(XPath('//button[@type="submit"]'))

    def find_text(self, text):
        self.input.type(text)
        self.find.click()


if __name__ == '__main__':
    ya_page = YaPage()
    ya_page.get()
    ya_page.find_text('autoui')
```

### Feature 1: Full support code inspections from IDE
From example above, if you write `ya_page`, put a dot, have a code inpection, 
write `find` and put a dot - you have code inpection again. Now you can select 
`click` function. Each element provides its own methods so you always know 
that, for example, for button you can't send keys. If you need this functionality, 
you can inherit from `Element` class and implement your own methods. Remember, 
that elements have special attribute `web_element` which is used to interact with 
webdriver.

### Feature 2: Default locator
You can use default locator to locate elements. Write it as a propherty of class that inherit `Element`.
```python
class CustomElement(Element):
    locator = XPath('.//a')
```
And and you don't need to write locator every time you want to put this custom element in your class.
```python
class Page(BasePage):
    custom_element = CustomElement()
```

### Feature 3: Elements can be located in other elements
pass

## History
Development in progress
