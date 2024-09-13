import asyncio

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from main import app

from tortoise import Tortoise

client = TestClient(app)


async def init_db():
    await Tortoise.init(
        db_url='sqlite://:memory:',
        modules={'models': ['res.database.classes']}
    )
    await Tortoise.generate_schemas()


asyncio.run(init_db())


@pytest_asyncio.fixture(scope='module', autouse=True)
async def initialize_tests():
    await init_db()
    yield
    await Tortoise.close_connections()


@pytest.fixture
def sample_order():
    return {
        "flat": 1,
        "dog_name": "Лаки",
        "dog_breed": "Чихуахуа",
        "time": "08:00",
        "date": "13.09.2024"
    }


@pytest.mark.asyncio
async def test_get_orders():
    response = client.get("/get_orders?date=13.09.2024")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_add_order(sample_order):
    response = client.post("/add_order", json=sample_order)
    assert response.status_code == 200
    result = response.json()
    assert result["dog_name"] == sample_order["dog_name"]
    assert result["date"] == sample_order["date"]


@pytest.mark.asyncio
async def test_add_order_with_existing_time():
    order = {
        "flat": 2,
        "dog_name": "Бим",
        "dog_breed": "Лабрадор",
        "time": "08:00",
        "date": "15.09.2024"
    }
    client.post("/add_order", json=order)
    client.post("/add_order", json=order)

    response = client.post("/add_order", json=order)

    assert response.status_code == 400
    assert response.json() == {"detail": "К сожалению, данное время уже занято"}
