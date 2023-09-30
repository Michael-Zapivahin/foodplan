from django.db import models
from django.db.models import Q

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


class DishQuerySet(models.QuerySet):
    def get_menu(self, subscription):
        allergies = subscription.subscription_allergies.all().prefetch_related('allergy')
        allergies_ids = [allergy.allergy.id for allergy in allergies.iterator()]
        menu = self.filter(~Q(allergy_tags__tag__in=allergies_ids))
        titles = []
        if subscription.breakfast:
            titles.append('Завтрак')
        if subscription.lunch:
            titles.append('Обед')
        if subscription.dinner:
            titles.append('Ужин')
        if subscription.dinner:
            titles.append('Десерт')
        menu = menu.filter(tags__tag__title__in=titles).distinct()
        return menu


class Dish(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    photo = models.ImageField(max_length=200, verbose_name='Photo', blank=True, null=True)
    calories = models.IntegerField(blank=True, null=True, verbose_name='Calories')

    objects = DishQuerySet.as_manager()
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
    cost = models.FloatField(blank=True, null=True, verbose_name='Cost')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='subscriptions')
    menu = models.ForeignKey(Menu, on_delete=models.DO_NOTHING, related_name='subscriptions')
    status = models.BooleanField(default=True, verbose_name='Active')

    def __str__(self):
        return f'{self.client.name} / ({self.title})'


class SubscriptionAllergy(models.Model):
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        verbose_name='Подписка',
        related_name='subscription_allergies',
    )
    allergy = models.ForeignKey(
        Allergy,
        on_delete=models.DO_NOTHING,
        verbose_name='Аллергия',
        related_name='subscription_allergies',
    )

    def __str__(self):
        return f'{self.allergy.title}'


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name='Title', unique=True)

    def __str__(self):
        return self.title


class DishTag(models.Model):
    dish = models.ForeignKey(
        Dish,
        on_delete=models.DO_NOTHING,
        related_name='tags',
        verbose_name='Dish',
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.DO_NOTHING,
        related_name='tags',
        verbose_name='Tag',
    )

    def __str__(self):
        return f'{self.dish.title}: {self.tag.title}'


class DishAllergyTag(models.Model):
    dish = models.ForeignKey(
        Dish,
        on_delete=models.DO_NOTHING,
        related_name='allergy_tags',
        verbose_name='Dish',
    )
    tag = models.ForeignKey(
        Allergy,
        on_delete=models.DO_NOTHING,
        related_name='allergy_tags',
        verbose_name='Allergy tag',
    )

    def __str__(self):
        return f'{self.dish.title}: {self.tag.title}'
