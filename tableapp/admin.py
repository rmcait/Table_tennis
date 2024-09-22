from django.contrib import admin

# Register your models here.
from .models import Table, WaitingList

admin.site.register(Table)
admin.site.register(WaitingList)