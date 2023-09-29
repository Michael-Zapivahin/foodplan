from django.db import models

# Create your models here.


class Menu(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    description = models.TextField(blank=True, null=True, verbose_name='Description')

    def __str__(self):
        return self.title


class Allergy(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    description = models.TextField(blank=True, null=True, verbose_name='Description')

    def __str__(self):
        return self.title


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
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='components', verbose_name='dish')

    def __str__(self):
        return self.title


class Client(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name')
    login = models.CharField(max_length=200, verbose_name='Login')
    password = models.CharField(max_length=200, verbose_name='Password')
    mail = models.EmailField(max_length=200, verbose_name='Mail', help_text='example@mail.ru')
    avatar = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.login})'


class Subscription(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    term = models.IntegerField(verbose_name='Term')
    breakfast = models.BooleanField(verbose_name='Breakfast', default=True)
    lunch = models.BooleanField(verbose_name='Lunch', default=True)
    dinner = models.BooleanField(verbose_name='Dinner', default=True)
    desserts = models.BooleanField(verbose_name='Desserts', default=True)
    persons_number = models.IntegerField(verbose_name='Numer of persons', default=1)
    allergy = models.ForeignKey(Allergy, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name='Allergy', related_name='subscriptions')
    cost = models.FloatField(blank=True, null=True, verbose_name='Cost')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='subscriptions')
    menu = models.ForeignKey(Menu, on_delete=models.DO_NOTHING, related_name='subscriptions')

    def __str__(self):
        return f'{self.client.name} / ({self.title})'











