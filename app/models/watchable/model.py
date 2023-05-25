from tortoise import Model, fields

class Watchable(Model):
    id = fields.CharField(pk=True, max_length=100)
    title = fields.CharField(max_length=100)
    img = fields.CharField(max_length=256, null=True)
    votes= fields.IntField(null=True)
    ranking = fields.CharField(max_length=30, null=True)
    last_ranking = fields.CharField(max_length=30, null=True)
    start_year = fields.CharField(max_length=30,null=True)
    end_year = fields.CharField(max_length=30,null=True)
    age = fields.CharField(max_length=30, null=True)
    runtime = fields.CharField(max_length=15, null=True)
    imdb_rating= fields.FloatField(null=True)
    metascore_rating= fields.FloatField(null=True)
    tomatoes_rating= fields.FloatField(null=True)
    type = fields.CharField(max_length=30)
    updated_at = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    description = fields.CharField(max_length=1000)

    class Meta:
        ordering=["type", "ranking"]