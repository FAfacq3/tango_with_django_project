from django.contrib import admin
from .models import Category, Page


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'custom_field')
    # additional customizations...


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


admin.site.register(Category)
admin.site.register(Page)
