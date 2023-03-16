from tortoise import Model, fields
from datetime import datetime

class Measurement(Model):
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(
        max_length=50,
    )
    created_at = fields.DatetimeField(default=datetime.now())

    class Meta:
        ordering=["id"]