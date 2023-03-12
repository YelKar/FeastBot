from typing import Iterable

from fetes import Feast


def day(day_: Iterable[Feast]):
    day_ = list(day_)
    result = f"<u><b>{day_[0].date}</b></u>\n"
    for ind, feast_ in enumerate(day_, 1):
        result += f"{ind}. {feast_.name}\n" \
                  f"<a href=\"{feast_.description_link}\">Подробнее</a>\n"
    return result


def feast(feast_: Feast, add_date=False):
    return (
        f"<b>{feast_.name}</b>\n" +
        (f"<i>{feast_.date}</i>\n" if add_date else "")
    )
