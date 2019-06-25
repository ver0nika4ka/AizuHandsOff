from django.contrib import admin

# Register models here.
from HandsOffApp.models import Owner, Category, Item

admin.site.register(Owner)
admin.site.register(Category)
admin.site.register(Item)