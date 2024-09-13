from datetime import datetime

import pytz


def get_localized_date() -> datetime.date:
    """
    Возвращает дату в московской времени. Полезно при запуске на VPS за пределами текущего часового пояса
    :return: datetime.date
    """
    local_tz = pytz.timezone("Europe/Moscow")
    return datetime.now(local_tz).date()
