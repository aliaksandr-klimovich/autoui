# autoui

[![Build Status](https://travis-ci.org/alex-klimovich/autoui.svg?branch=master)](https://travis-ci.org/alex-klimovich/autoui)

Web site automation testing framework.

The goal is to show how to implement custom page object pattern in python. 
This project was inspired by `webium` project and structural patterns in java.
It is not designed for production usage. It's only my own approach to test web sites.

## Requirements
- python 2.7 or 3
- selenium
- nose (for internal tests)
- mock (for internal tests)
- cherrypy (for internal tests)
- chromedriver executable (for internal tests)

See `requirements.txt`.

## Usage
### Basic test
```python
from autoui.base_page import BasePage
from autoui.elements.simple import Button, Input
from autoui.locators import XPath, ID


class YaPage(BasePage):
    url = 'http://ya.ru'
    input = Input(ID('text'))
    find = Button(XPath('//button[@type="submit"]'))

    def find_text(self, text):
        self.input().type(text)
        self.find().click()


if __name__ == '__main__':
    ya_page = YaPage()
    ya_page.get()
    ya_page.find_text('autoui')
```

### Feature 1: Support code inspections from IDE
From example above, if you write `ya_page`, put a dot, have a code inspection, 
write `find()` and put a dot - you have code inspection again. Now you can select 
`click()` function. Each element provides its own methods so you always know 
that, for example, for button you can't send keys. If you need this functionality, 
you can inherit from `Element` class and implement your own methods. Remember, 
that elements have special attribute `web_element` which is used to interact with 
webdriver.

### Feature 2: Default locator
You can use default locator to locate elements. Write it as a property of class that inherit `Element`.
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
By default `autoui` looks for new element with parent if exists.
For example:
```python
class Section(Element):
    locator = XPath('section')
    element = Input(XPath('element'))

class Page:
    section = Section()
```
`Page().section().element` will look for section with driver and element with section.
If you want to find element with driver instead of section - use
`search_with_driver = True` attribute for current section. You can use this trick:
```python
class Section(Element):
    locator = XPath('section')
    element = Input(XPath('element'))
    element.search_with_driver = True
```
or
```python
class Section(Element):
    locator = XPath('section')
    element = Input(XPath('element'), search_with_driver=True)
```
or inside an element
```python
class CustomElement(Element):
    search_with_driver = True
```
to find single element in section with driver.


### Feature 4: Filling elements
To do fill fields more easy you can use dict with predefined values.
Create your custom element, i.e. inherit from `Element` class.
Then inherit from Filling class.
Note, you must override `fill` or/and `get_state` method(s)
if you want to do some special.

```python
class Section2(Element, Filling):
    locator = XPath('section2')
    s2_el1 = Input(XPath('s2_el1'))
    s2_el2 = Input(XPath('s2_el2'))

class Section1(Element, Filling):
    locator = XPath('section1')
    stop_propagation = True
    section2 = Section2()
    s1_el1 = Input(XPath('s1_el1'))

class Page:
    section1 = Section1()
```

Now you can access section2 with `Page().section1().section2()`.
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
For example, you can access `s1_el1` with `Page().section1().s1_el1`
and `s2_el2` with `Page().section1().section2().s2_el2`.
Now if you write `Page().section1.fill(dict_to_fill)` than
element `s1_el1` will be filled with `s1_el1_value`,
element `s2_el1` will be filled with `s2_el1_value` and
element `s2_el2` will be filled with `s2_el2_value`.

After all this manipulations you can get your dict by writing
`dict_with_state = Page().section1.get_state()` and continue working with it.

You can tell to your element that fill propagation will be stopped
by filling the attribute: `stop_propagation = True` in custom element class.
After that, if section contains other elements, i.e. sections,
than the algorithm will not look inside them.

### Feature 5: Can pass custom waiter to the element
Use mixins for `Element` and `Elements` classes.

### Feature 6: Finding parent stale element is the default behaviour

Realized in `find` method of `Element` class.

Let's imagine that we have next situation.
I have `Page` class, it contains `Section` class
and the `Section` class contains `Element` inside.
I do some work inside `Element` class having `web_element` reference.
But in the middle of my work the element `Section` updates.
Than I'll have `StaleElementReferenceException` from `finder`.
But what exactly I want to have? That the element can be found once again!
If `Section` is updated than `find` method tries to obtain parent object
to find it. After all `Section` will be found and I'll have chance to continue
working with `Element`.

### Feature 7: Attach elements to their parents

Added possibility to attach elements to other classes at runtime.

```python
class ParentElement(Element):
    locator = ID('ParentElement')

class ChildElement(Element):
    locator = ID('ChildElement')

parent_element = ParentElement()
parent_element.find()
child_element = ChildElement(parent=parent_element)
child_element.find()
```

This feature has not been tested in depth.
