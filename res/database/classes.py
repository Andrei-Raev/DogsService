from tortoise import fields, models


class DogWalkORM(models.Model):
    id = fields.IntField(primary_key=True)
    flat = fields.IntField(description="Номер квартиры")
    dog_name = fields.CharField(max_length=255, description="Кличка животного")
    dog_breed = fields.CharField(max_length=255, description="Порода животного")
    time = fields.CharField(max_length=5, description="Время прогулки в формате ЧЧ:ММ с минутами равными 00 или 30")
    date = fields.CharField(max_length=10, description="Дата прогулки в формате ДД.ММ.ГГГГ")

    class Meta:
        table = "dog_walk"
