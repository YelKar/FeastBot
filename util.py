from calendar import monthrange, month_name
from datetime import datetime, timedelta
from typing import Union, Optional
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


reference = (
    "Справка"
)


class KeyBoard:
    @classmethod
    def day_list(cls, month: Optional[Union[str, int]] = None):
        if isinstance(month, str):
            month = datetime.strptime(month, "%B").month

        result = []
        if month is None:
            date = datetime.now()
            day_count = monthrange(2024, date.month)[1]
        else:
            date = datetime(2024, month, 1)
            day_count = monthrange(2024, month)[1]

        for n in range(day_count):
            result.append((date.day, date.month))
            date += timedelta(1)

        return result

    @classmethod
    def month(cls, month: Optional[Union[str, int]] = None):
        days = cls.day_list(month)
        kb = InlineKeyboardMarkup(row_width=7)
        for row in chunks(days, 7):
            kb.add(*map(lambda day: InlineKeyboardButton(day[0], callback_data=f"send_day_{day[0]}.{day[1]}"), row))

        return kb

    @classmethod
    def year(cls):
        kb = InlineKeyboardMarkup(row_width=3)
        for i, row in enumerate(chunks(list(month_name)[1:], 3)):
            kb.add(*[InlineKeyboardButton(month, callback_data=f"send_month_{i * 3 + j}") for j, month in enumerate(row, 1)])
        return kb


def chunks(arr, chunk_size):
    for i in range(0, len(arr), chunk_size):
        yield arr[i:i + chunk_size]


if __name__ == '__main__':
    print(KeyBoard.year())
