from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Union, TextIO
from io import TextIOWrapper

from bs4 import BeautifulSoup
from cloudscraper import create_scraper


@dataclass
class Feast:
    name: str
    date: str
    description: str
    description_link: str


class Feasts:
    link: Union[str, None] = "https://celebratoday.com/ru/"
    timezone: timezone = timezone(timedelta(hours=3), "МСК")

    def __init__(self, html: Union[str, None] = None):
        if html is None:
            self.soup = None
        else:
            self.soup = None if html is None else BeautifulSoup(html, "html.parser")

    @classmethod
    def get(cls, link: Union[TextIOWrapper, str, TextIO, None] = None):
        if isinstance(link, TextIOWrapper):
            html = link.read().strip()
        elif isinstance(link, str):
            html = cls.get_html(link)
        else:
            raise TypeError("link must be string or OI")
        obj = cls(html)
        if isinstance(link, str):
            obj.link = link
        return obj

    @staticmethod
    def to_feast(main_block=None) -> Feast:
        main_block = main_block
        description = main_block.select_one("div.hidden").text.strip()
        name_block = main_block.select_one("div.flex.flex-col.gap-3")
        description_link = main_block.select_one("div.flex.justify-between > a").attrs.get("href")

        name = name_block.select_one("a > h3").text.strip()
        day = " ".join(name_block.select_one("span.inline-block.text-sm.leading-none").text.split())

        return Feast(name, day, description, description_link)

    def today(self):
        return self.get_day(datetime.now(self.timezone).date())

    def get_day(self, day: date):
        link = self.get_day_link(day)
        html = self.get_html(link)
        soup = BeautifulSoup(html, "html.parser")

        feast_blocks = soup.select(
            "div.flex.flex-col.border.rounded-lg.group"
        )
        for block in feast_blocks:
            yield self.to_feast(block)

    def get_day_link(self, day: date):
        if not isinstance(self.link, str):
            return None
        feast_month = day.strftime("%B").lower()
        feast_day = day.day
        return f"{self.link.strip('/')}/events/{feast_month}/{feast_day:0>2}"

    @staticmethod
    def get_html(link):
        if link is None:
            return None
        scraper = create_scraper()
        with scraper.get(link) as res:
            html = res.text.strip()
        return html

    def __getitem__(self, item):
        """
        if item is integer
        :return today first Feast
        if item is any slice
        if [feast_num:relative_day=today]
        :return Feast by feast_num in relative_day
        if [feast_num:day:month]
        :return Feast by feast_num in day.month

        :param item:
        """
        if isinstance(item, int):
            try:
                return list(self.today())[item]
            except IndexError:
                return None
        elif isinstance(item, slice):
            if item.step is None:
                dt = datetime.now(self.timezone) + timedelta(days=item.stop or 0)
                day = list(self.get_day(dt.date()))
                if item.start is None:
                    return day
                return day[item.start]
            else:
                day = list(self.get_day(date(2023, item.step, item.stop)))
                if item.start is None:
                    return day
                else:
                    return day[item.start]
