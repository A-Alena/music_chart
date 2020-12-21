from django.db import models

class Musician(models.Model):
    auth_name = models.TextField()
    song_name = models.TextField()
    chart_position = models.IntegerField()

    class Meta:
        db_table = 'musicians'