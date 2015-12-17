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

### Feature 3: Element can be located in/with other element
in progress ...

### Feature 4: Fillable elements
To do fill fields more easy you can use dict with predefined values.
Create your custom element, i.e. inherit from `Element` class.
Then inherit from Fillable class.
Note, you must override `fill` or/and `get_state` method(s)
if you want to do some special.

```python
class Section2(Element, Fillable):
    locator = XPath('section2')
    s2_el1 = Input(XPath('s2_el1'))
    s2_el2 = Input(XPath('s2_el2'))

class Section1(Element, Fillable):
    locator = XPath('section1')
    stop_propagation = True
    section2 = Section2()
    s1_el1 = Input(XPath('s1_el1'))

class Page:
    section1 = Section1()
```

Now you can access section2 with `Page.section1.section2`.
Let's create a dict to pass to `fill` method of `Section1`:

```python
dict_to_fill = {
    's1_el1': 's1_el1_value',
    'section2': {
        's2_el1': 's2_el1_value',
        's2_el2': 's2_el2_value',
    }
}
```

Here keys are element names and values are other element names or values to fill.
For example, you can access `s1_el1` with `Page.section1.s1_el1`
and `s2_el2` with `Page.section1.section2.s2_el2`.
Now if you write `Page.section1.fill(dict_to_fill)` than
element `s1_el1` will be filled with `s1_el1_value`,
element `s2_el1` will be filled with `s2_el1_value` and
element `s2_el2` will be filled with `s2_el2_value`.

After all this manipulations you can get your dict by writing
`dict_with_state = Page.section1.get_state()` and continue working with it.

You can tell to your element that fill propagation will be stopped
by filling the attribute: `stop_propagation = True` in custom element class.
After that, if section contains other elements, i.e. sections,
than the algorithm will not look inside them.


### Feature 5: Can pass custom waiter to the element
in progress ...
