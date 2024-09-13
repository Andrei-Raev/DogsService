import pytest
from datetime import datetime
from pydantic import ValidationError
from res.schemas import DogWalk


def mock_get_localized_date():
    return datetime.strptime("01.01.2022", "%d.%m.%Y").date()


def test_valid_dogwalk():
    # Проверяем валидные данные
    dogwalk = DogWalk(flat=10, dog_name="Шарик", dog_breed="Лабрадор", time="08:00", date="10.09.2025")
    assert dogwalk.flat == 10
    assert dogwalk.dog_name == "Шарик"
    assert dogwalk.dog_breed == "Лабрадор"
    assert dogwalk.time == "08:00"
    assert dogwalk.date == "10.09.2025"


def test_invalid_time_format():
    # Неверный формат времени
    with pytest.raises(ValidationError):
        DogWalk(flat=1, dog_name="Лаки", dog_breed="Чихуахуа", time="08:15", date="10.09.2025")

    # Время раньше 7:00
    with pytest.raises(ValidationError):
        DogWalk(flat=1, dog_name="Лаки", dog_breed="Чихуахуа", time="06:30", date="10.09.2025")

    # Время позже 23:00
    with pytest.raises(ValidationError):
        DogWalk(flat=1, dog_name="Лаки", dog_breed="Чихуахуа", time="23:30", date="10.09.2025")


def test_invalid_date_format(mocker):
    # Мокаем get_localized_date для тестирования
    mocker.patch('res.utils.get_localized_date', mock_get_localized_date)

    # Неверный формат даты
    with pytest.raises(ValidationError):
        DogWalk(flat=1, dog_name="Лаки", dog_breed="Чихуахуа", time="08:00", date="2025-09-10")

    # Дата из прошлого
    with pytest.raises(ValidationError):
        DogWalk(flat=1, dog_name="Лаки", dog_breed="Чихуахуа", time="08:00", date="10.09.2020")

    with pytest.raises(ValidationError):
        DogWalk(flat=1, dog_name="Лаки", dog_breed="Чихуахуа", time="23:30", date="10.09.2005")
