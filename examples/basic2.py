# coding=utf-8
from autoui.base_page import BasePage
from autoui.driver import get_driver
from autoui.elements.abstract import Element
from autoui.elements.implemented import Links, Text
from autoui.locators import XPath, CSS


class Today(Element):
    locator = XPath('./tbody/tr/td[1]')
    day = Text(CSS('.day'))
    now = Text(CSS('.now'))
    week = Text(CSS('.week'))
    month = Text(CSS('.month'))


class FiveDaysForecast(Element):
    locator = XPath('/html/body/div[1]/div[5]/table')
    today = Today()


class MinskTheBy(BasePage):
    url = 'http://minsk.the.by/'
    links = Links(XPath('//a'))
    five_days_forecast = FiveDaysForecast()

    def get_all_links(self):
        return self.links.find().hrefs


if __name__ == '__main__':
    get_driver().set_window_size(800, 1200)
    minsk_the_by = MinskTheBy()
    minsk_the_by.get()
    print minsk_the_by.get_all_links()
    print u'Сегодня ' + minsk_the_by.five_days_forecast.find().today.find().day.find().text + u' число месяца ' + \
        minsk_the_by.five_days_forecast.find().today.find().month.find().text
    get_driver().quit()
