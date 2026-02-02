from django.db import models
from django.contrib.auth.models import User
# Сигнал для автоматического создания профиля при создании пользователя
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Ingridients(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название ингридиента')
    is_allergen = models.BooleanField()

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название блюда')
    price = models.FloatField(null=True, blank=True, verbose_name='Стоимость')
    about = models.TextField(null=True, blank=True, verbose_name='Описание')
    in_menu = models.BooleanField(default=False, verbose_name='В архиве')
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='Категория'
    )
    ingridients = models.ManyToManyField(
        Ingridients, 
        blank=True, 
        verbose_name='Ингридиенты'
    )
    
    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class СomplexDish(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название комплекса')
    price = models.FloatField(null=True, blank=True, verbose_name='Стоимость')
    about = models.TextField(null=True, blank=True, verbose_name='Описание')
    in_menu = models.BooleanField(default=False, verbose_name='В архиве' )
    dishes = models.ManyToManyField(
        Dish, 
        blank=True, 
        verbose_name='Блюда в комплексе'
    )
    
    class Meta:
        verbose_name = 'Комплекс'
        verbose_name_plural = 'Комплексы'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Application(models.Model):
    
    STATUS_CHOICES = (
        ("NEW", "Новый"),
        ("DONE", "Оплата проведена"),
    )

    name = models.CharField(max_length=100, unique=True, verbose_name='Название заявки')
    date = models.DateField(null=True, blank=True, verbose_name='Дата')
    amount = models.FloatField(null=True, blank=True, verbose_name='Стоимость')
    select_dishes = models.ForeignKey(
    Dish, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='Выбор блюд'
    )
    status = models.CharField(max_length=9,
                    choices=STATUS_CHOICES,
                 verbose_name='Статус',
                  default="NEW")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления', null=True, blank=True)

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='Автор заказа',
        related_name='applications',
        null=True, blank=True,
    )

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['name']
    
    def __str__(self):
        return self.name



class Feedback_category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    
    class Meta:
        verbose_name = 'Категория отзыва'
        verbose_name_plural = 'Категории отзыва'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Feedback(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название отзыва')
    sender = models.CharField(max_length=100, unique=True, verbose_name='Имя отправителя')
    about = models.TextField(null=True, blank=True, verbose_name='Описание')
    is_good = models.FloatField(null=True, blank=True, verbose_name='Оценка')
    feedback_category = models.ForeignKey(
        Feedback_category,
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='Категория отзыва'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название меню')
    complex_dishes = models.ManyToManyField(
        СomplexDish, 
        blank=True, 
        verbose_name='Комплекс в меню'
    )
    dishes = models.ManyToManyField(
        Dish, 
        blank=True, 
        verbose_name='Блюда в меню'
    )

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Profile(models.Model):
    """Профиль пользователя для хранения дополнительных данных"""
   
    STATUS_CHOICES = (
        ("povar", "Повар"),
        ("student", "Школьник"),
        ("parent", "Родитель"),
        ("admin", "Админ"),
    )
   
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile'
    )
    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    class_group = models.CharField(max_length=100, verbose_name='учебный класс')
    phone = models.CharField(max_length=100, verbose_name='телефон')
    parent_phone = models.CharField(max_length=100, verbose_name='телефон родителей')
    status = models.CharField(max_length=9,
                    choices=STATUS_CHOICES,
                 verbose_name='Статус',
                  default="povar")
    balans = models.FloatField(null=True, blank=True, verbose_name='Баланс денег')
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
    
    def __str__(self):
        return f"Профиль {self.user.username}"



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()