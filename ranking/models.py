from django.db import models

# Create your models here.


class Client(models.Model):
    cli = models.CharField(max_length=20, unique=True)
    score = models.IntegerField(db_index=True)
