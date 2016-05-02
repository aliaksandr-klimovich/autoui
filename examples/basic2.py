# coding=utf-8
from autoui.base_page import BasePage
from autoui.driver import get_driver
from autoui.elements.abstract import Element
from autoui.elements.simple import Links, Text
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
    links = Links(XPath('//a[starts-with(@href, "http")]'))
    five_days_forecast = FiveDaysForecast()

    def get_all_links(self):
        return self.links().hrefs


if __name__ == '__main__':
    d = get_driver()
    d.set_window_size(800, 600)
    forecast_today = MinskTheBy().get().five_days_forecast().today()
    print(u'Сегодня ' + forecast_today.day().text.strip() + u' число месяца ' + forecast_today.month().text.strip())
    d.quit()
