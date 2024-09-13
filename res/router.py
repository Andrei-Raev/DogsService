from fastapi import Query, HTTPException
from fastapi.routing import APIRouter
from res.schemas import DogWalk
from res.database.classes import DogWalkORM

router = APIRouter()


@router.get("/get_orders", response_model=list[DogWalk], tags=["Orders"], summary="Get all orders by date")
async def get_orders(
        date: str = Query(..., title="Date", description="Дата в формате dd.mm.yyyy", examples=["13.09.2024"],
                          pattern=r"(0?[1-9]|[12][0-9]|3[01])\.(0?[1-9]|1[0-2])\.20\d{2}")) -> list[DogWalk]:
    """
    Ручка для получения списка всех прогулок по дате
    :param date: Дата в формате dd.mm.yyyy
    :return: Список прогулок
    """
    return await DogWalkORM.filter(date=date).all()


@router.post("/add_order", response_model=dict, tags=["Orders"], summary="Add order")
async def add_order(order: DogWalk):
    """
    Ручка для добавления прогулки пользователями
    :param order: Заявка на прогулку
    :return: Статус добавления заявки
    """
    if await DogWalkORM.filter(date=order.date, time=order.time).count() >= 2:  # Если Пётр и Антон оба заняты
        raise HTTPException(status_code=400, detail="К сожалению, данное время уже занято")
    await DogWalkORM.create(**order.model_dump())
    return {"detail": "OK"}
