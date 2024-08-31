from django.db import models

# Create your models here.


class Table(models.Model):
    number = models.IntegerField(unique=True)  # 卓球台の番号
    is_occupied = models.BooleanField(default=False)  # 利用中かどうかを表す

    def __str__(self):
        return f"Table {self.number}"