from django.db import models

# Create your models here.


class Table(models.Model):

    number = models.IntegerField(unique=True)  # 卓球台の番号
    is_occupied = models.BooleanField(default=False)  # 利用中かどうかを表す


    def __str__(self):
        return f"Table {self.number}"


class WaitingList(models.Model):
    TIME_SLOTS = [
        ("9時 ~ 11時", "9時 ~ 11時"),
        ("11時 ~ 13時", "11時 ~ 13時"),
        ("13時 ~ 15時", "13時 ~ 15時"),
        ("15時 ~ 17時", "15時 ~ 17時"),
        ("17時 ~ 19時", "17時 ~ 19時"),
        ("19時 ~ 21時", "19時 ~ 21時"),
    ]

    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    next_is_occupied = models.BooleanField(default=False)
    time_slot = models.CharField(max_length=20, choices=TIME_SLOTS, blank=True, null=True)
    # time_slot = models.CharField(max_length=20, choices=TIME_SLOTS, default="9時 ~ 11時")  # デフォルトを指定

    # def __str__(self):
        # return f"Waiting List for Table {self.table.number} ({self.time_slot})"

