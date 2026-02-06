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
    name = models.CharField(max_length=100, unique=True, verbose_name='Название ингредиента')
    is_allergen = models.BooleanField()
    price = models.FloatField(null=True, blank=True, verbose_name='Стоимость')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
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


class Abonement(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название абонемента')
    price = models.FloatField(null=True, blank=True, verbose_name='Стоимость абонемента')

    dishes_in_abonement = models.ManyToManyField(
        Dish, 
        blank=True, 
        verbose_name='Блюда в абонементе'
    )

    amount_of_dishes = models.FloatField(null=True, blank=True, verbose_name='Количество блюд')

    complex_in_abonement = models.ManyToManyField(
        СomplexDish, 
        blank=True, 
        verbose_name='Комплексы в абонементе'
    )

    amount_of_complex = models.FloatField(null=True, blank=True, verbose_name='Количество комплексов')
    
    class Meta:
        verbose_name = 'Абонемент'
        verbose_name_plural = 'Абонементы'
        ordering = ['name']
    
    def __str__(self):
        return self.name



class Purchase(models.Model):

    STATUS_POVAR = (
        ("NEW", "Новый"),
        ("DONE", "Заказ выдан"),
    )

    STATUS_OPLATY = (
        ("NEW", "Новый"),
        ("IN_PROGRESS", "Оплата проведена"),
        ("DONE", "Заказ получен"),
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.RESTRICT, 
        verbose_name='Кто заказал еду',
        related_name='purchases',
        null=True, blank=True,
    )
    name = models.CharField(max_length=100, unique=True, verbose_name='Название покупки',null=True, blank=True)
    dishes_in_purchase = models.ManyToManyField(
        Dish, 
        blank=True, 
        verbose_name='Блюда'
    )

    complex_in_purchase = models.ManyToManyField(
        СomplexDish, 
        blank=True, 
        verbose_name='Комплексы'
    )


    price = models.FloatField(null=True, blank=True, verbose_name='Стоимость')

    status_povar = models.CharField(max_length=20,
                    choices=STATUS_POVAR,
                 verbose_name='Статус от повара',
                  default="NEW")
    
    status_oplaty = models.CharField(max_length=20,
                    choices=STATUS_OPLATY,
                 verbose_name='Статус оплаты',
                  default="NEW")
    
    class Meta:
        verbose_name = 'Покупка еды учеником'
        verbose_name_plural = 'Покупки еды учеником'
        ordering = ['name']
    
    def __str__(self):
         return f"{self.id} - {self.user}"


class Profile(models.Model):
    """Профиль пользователя для хранения дополнительных данных"""
   
    STATUS_CHOICES = (
        ("povar", "Повар"),
        ("zakup", "Закупщик"),
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
    class_group = models.CharField(null=True, blank=True, max_length=100, verbose_name='учебный класс')
    phone = models.CharField(null=True, blank=True, max_length=100, verbose_name='телефон')
    parent_phone = models.CharField(null=True, blank=True, max_length=100, verbose_name='телефон родителей')
    status = models.CharField(max_length=9,
                    choices=STATUS_CHOICES,
                 verbose_name='Статус',
                  default="student")
    balans = models.FloatField(null=True, blank=True, verbose_name='Баланс денег')
    balans_obedov = models.IntegerField(null=True, blank=True, verbose_name='Баланс обедов')
    balans_dishes = models.IntegerField(null=True, blank=True, verbose_name='Баланс блюд')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
    
    def __str__(self):
        return f"Профиль {self.user.username}"


class Application_student(models.Model):
    STATUS_CHOICES = (
        ("NEW", "Новый"),
        ("DONE", "Баланс пополнен"),
    )
    
    date = models.DateTimeField(null=True, blank=True, verbose_name='Дата заявки учащегося')
    amount = models.FloatField(null=True, blank=True, verbose_name='Сумма пополнения')

    abonement = models.ForeignKey(
        Abonement, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='Абонемент'
    )

    user = models.ForeignKey(
        Profile, 
        on_delete=models.RESTRICT, 
        verbose_name='Кому пополняем баланс',
        related_name='applications_add_balans',
        null=True, blank=True,
    )
    admin = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        verbose_name='Кто обрабатывает заявку',
        null=True, blank=True,
    )

    status = models.CharField(max_length=9,
                    choices=STATUS_CHOICES,
                 verbose_name='Статус',
                  default="NEW")
    name = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name='Название заявки учащегося')
    

    class Meta:
        verbose_name = 'Пополнение баланса'
        verbose_name_plural = 'Пополнения баланса'
        ordering = ['name']
    
    def __str__(self):
         return f"{self.id} - {self.name}"


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





class Application(models.Model):
    
    STATUS_CHOICES = (
        ("NEW", "Новый"),
        ("COST", "Расчет стоимости"),
        ("PAY", "Оплечен"),
        ("CONFIRMED", "Подтвержден"),
        ("DONE", "Получен"),
    )

    name = models.CharField(max_length=100, unique=True, verbose_name='Название заявки')
    date = models.DateField(null=True, blank=True, verbose_name='На какую дату нужен заказ')
    amount = models.FloatField(null=True, blank=True, verbose_name='Стоимость')
    menu = models.ManyToManyField(Menu, 
        blank=True, null=True,
        verbose_name='Комплекс в меню'
    )
    ingridients = models.ManyToManyField(Ingridients, 
        blank=True, null=True,
        verbose_name='Ингредиент'
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
        verbose_name = 'Заявка на закупку повара'
        verbose_name_plural = 'Заявки на закупку повара'
        ordering = ['name']
    
    def __str__(self):
        return self.name




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()