from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название блюда')
    price = models.FloatField(null=True, blank=True, verbose_name='Стоимость')
    about = models.TextField(null=True, blank=True, verbose_name='Описание')
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='Категория'
    )
    
    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ['name']
    
    def __str__(self):
        return self.name
