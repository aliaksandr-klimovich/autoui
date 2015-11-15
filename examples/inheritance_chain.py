from autoui.base import BasePage, BaseSection
from autoui.element.common import Text
from autoui.find import Find
from autoui.locator import CSS


class ForecastDateSection(BaseSection):
    day = Find(Text, CSS('p.day'))


class Forecast8DaysSection(BaseSection):
    forecast_date_section = Find(ForecastDateSection, CSS('.plp1 > table'))


class MinskTheByPage(BasePage):
    url = 'http://minsk.the.by/'
    forecast_8_days_section = Find(Forecast8DaysSection, CSS('.p1 > table'))


if __name__ == '__main__':
    MinskTheByPage.get()
    print MinskTheByPage.forecast_8_days_section.forecast_date_section.day.text
