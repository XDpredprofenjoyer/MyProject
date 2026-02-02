from django.db import models

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