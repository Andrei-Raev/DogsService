import re
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from res.utils import get_localized_date


class DogWalk(BaseModel):
    flat: int = Field(..., gt=0, description="Номер квартиры")
    dog_name: str = Field(..., description="Кличка животного", max_length=255, min_length=2)
    dog_breed: str = Field(..., description="Порода животного", max_length=255, min_length=2)
    time: str = Field(..., description="Время прогулки в формате ЧЧ:ММ с минутами равными 00 или 30",
                      examples=["11:00"])
    date: str = Field(..., description="Дата прогулки в формате ДД.ММ.ГГГГ", examples=["13.09.2024"])

    @field_validator('time')
    @classmethod
    def check_time_format(cls, v):
        """
        Проверяет корректность введенного времени
        :param v: Значение
        :return: Обработанное значение
        """
        if not re.match(r'(0?[0-9]|1[0-9]|2[0-3]):(00|30)', v):
            raise ValueError('Время должно быть в формате ЧЧ:ММ с минутами равными 00 или 30')

        if int(v.split(':')[0]) < 7:
            raise ValueError('Время прогулки возможно назначить от 7:00 включительно')

        elif int(v.split(':')[0]) == 23 and int(v.split(':')[1]) == 30:
            raise ValueError('Время прогулки возможно назначить до 23:00 включительно')

        return v

    @field_validator('date')
    @classmethod
    def check_date_format(cls, v):
        """
        Проверяет корректность введенной даты
        :param v: Значение
        :return: Обработанное значение
        """
        if not re.match(r"(0?[1-9]|[12][0-9]|3[01])\.(0?[0-9]|1[0-2])\.20\d{2}", v):
            raise ValueError('Дата должна быть в формате ДД.ММ.ГГГГ')

        date_obj = datetime.strptime(v, "%d.%m.%Y").date()
        if date_obj < get_localized_date():
            raise ValueError('По законам физики дата не может быть из прошлого')

        return v
