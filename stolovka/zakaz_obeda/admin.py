from django.contrib import admin

from .models import Category, Dish


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для категории"""
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 20



@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    """Админка для блюд"""
    list_display = ('name', 'price', 'about', 'category')
    search_fields = ('name',)
    list_per_page = 20
    list_filter = ('category',)