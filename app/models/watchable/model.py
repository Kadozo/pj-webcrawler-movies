from tortoise import Model, fields

class Watchable(Model):
    id = fields.IntField(pk=True, index=True)
    title = fields.CharField(max_length=100)
    ranking = fields.IntField()
    star_year = fields.IntField(null=True)
    end_year = fields.IntField(null=True)
    age = fields.CharField(max_length=10, null=True)
    runtime = fields.CharField(max_length=15, null=True)
    imdb_rating= fields.CharField(max_length=5, null=True)
    metascore_rating= fields.CharField(max_length=5, null=True)
    tomatoes_rating= fields.CharField(max_length=5, null=True)
    type = fields.CharField(max_length=10)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        ordering=["type", "start_year"]