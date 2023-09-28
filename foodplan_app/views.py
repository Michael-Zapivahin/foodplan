from django.shortcuts import render
from .models import Dish, Component


def index(request):
    return render(request, 'index.html')


def card(request):
    dish = Dish.objects.all()[0]
    context = {
        'title': dish.title,
        'descripion': dish.description,
        'components': dish.components.all(),
        'calories': dish.calories,
        'photo': dish.photo,
    }
    dish = {'dish': context}
    return render(request, 'card.html', context=dish)
