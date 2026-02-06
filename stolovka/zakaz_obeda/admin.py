from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import Category, Dish, Ingridients, Menu, Application, Feedback, Feedback_category, СomplexDish, Application_student, Profile, Purchase, Abonement


class BalansInline(admin.StackedInline):
    """Инлайн для отображения пополнения баланса пользователя"""
    model = Application_student
    extra = 1
    fields = ('name', 'date', 'amount', "abonement",'user', "status")

class CustomUserAdmin(admin.ModelAdmin):
    inlines = [BalansInline]
    raw_id_fields = ("user",)
    list_display = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'user__is_staff', "class_group", "balans_obedov", "balans")
    list_filter = ('status', "balans_obedov", "balans" )
    search_fields = ('user__last_name',)
  #  readonly_fields = ('balans',)

#admin.site.unregister(User)
admin.site.register(Profile, CustomUserAdmin)


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
    list_display = ('name', 'date', 'amount', 'user',)
    search_fields = ('name',)
    list_per_page = 20
    readonly_fields = ('created_at', "updated_at", "amount",)
    filter_horizontal = ("menu", "ingridients")


@admin.register(Application_student)
class Application_studentAdmin(admin.ModelAdmin):
    """Админка для пополнения баланса"""
    list_display = ("id", 'name', 'date', 'amount', "abonement",'user', "status")
    search_fields = ('name', "user__email")
    list_per_page = 20
    list_filter = ('status', )
    raw_id_fields = ("user", "admin")
    


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


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    """Админка для покупок"""
    list_display = ('name', 'price', 'status_povar', 'status_oplaty',)
    search_fields = ('name',)
    list_per_page = 20
    list_filter = ('dishes_in_purchase', 'complex_in_purchase', 'status_povar', 'status_oplaty',)
    filter_horizontal = ("dishes_in_purchase", "complex_in_purchase")
    raw_id_fields = ("user",)


@admin.register(Abonement)
class AbonementAdmin(admin.ModelAdmin):
    """Админка для абонементов"""
    list_display = ('name', 'price', 'amount_of_dishes', 'amount_of_complex',)
    search_fields = ('name',)
    list_per_page = 20
    list_filter = ('dishes_in_abonement', 'complex_in_abonement',)
    filter_horizontal = ('dishes_in_abonement', 'complex_in_abonement',)


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