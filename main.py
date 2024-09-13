from fastapi import FastAPI
import uvicorn

from res.router import router as dog_service_router
from tortoise.contrib.fastapi import RegisterTortoise
from settings import TORTOISE_ORM

app = FastAPI(title="Dog Service", version="1.0.0",
              description="Сервис для управления графиком прогулок с собаками")
app.include_router(dog_service_router)

# Инициализация базы данных
RegisterTortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
