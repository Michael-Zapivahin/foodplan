from django.db import models

# Create your models here.


class Dish(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    photo = models.ImageField(max_length=200, verbose_name='Photo', blank=True, null=True)
    calories = models.IntegerField(blank=True, null=True, verbose_name='Calories')

    def __str__(self):
        return self.title


class Component(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    weight = models.IntegerField(blank=True, null=True, verbose_name='weight')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='dishes', verbose_name='dish')

    def __str__(self):
        return self.title
