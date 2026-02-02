from django.contrib import admin

from .models import Category, Dish, Ingridients, Menu, Application, Feedback, Feedback_category, СomplexDish


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для категории"""
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 20


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """Админка для меню"""
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 20
    filter_horizontal = ("complex_dishes", "dishes")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Админка для заявки"""
    list_display = ('name', 'date', 'amount', 'select_dishes',)
    search_fields = ('name',)
    list_per_page = 20


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    """Админка для блюд"""
    list_display = ('name', 'price', 'about', 'in_menu', 'category')
    search_fields = ('name',)
    list_per_page = 20
    list_filter = ('category', "ingridients")
    filter_horizontal = ("ingridients",)


@admin.register(СomplexDish)
class СomplexDishAdmin(admin.ModelAdmin):
    """Админка для комплексных обедов или завтраков"""
    list_display = ('name', 'price', 'about', 'in_menu')
    search_fields = ('name',)
    list_per_page = 20
    list_filter = ('dishes',)
    filter_horizontal = ("dishes",)


@admin.register(Ingridients)
class IngridientsAdmin(admin.ModelAdmin):
    """Админка для ингридиентов"""
    list_display = ('name', 'is_allergen')
    search_fields = ('name',)
    list_per_page = 20


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Админка для отзывов"""
    list_display = ('name', 'sender', 'about', 'is_good', 'feedback_category')
    search_fields = ('name',)
    list_per_page = 20
    list_filter = ('feedback_category',)


@admin.register(Feedback_category)
class Feedback_categoryAdmin(admin.ModelAdmin):
    """Админка для категорий отзывов"""
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 20