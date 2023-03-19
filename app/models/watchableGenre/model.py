from tortoise import Model, fields

class WatchableGenre(Model):
    id = fields.IntField(pk=True, index=True)
    genre = fields.ForeignKeyField("models.Genre", related_name="genres")
    watchable = fields.ForeignKeyField("models.Watchable", related_name="watchable")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        ordering=["id"]