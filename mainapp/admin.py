from django.contrib import admin
from mainapp import models


@admin.register(models.Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ('name', 'id')

@admin.register(models.Category)
class CategoryProduct(admin.ModelAdmin):
    list_display = ('name', 'id', 'parent', 'level', 'road')
    prepopulated_fields = {'slug': ('name',)}

