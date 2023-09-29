from django.shortcuts import render

from .models import Dish, Allergy
from .db_operations import create_subscription



def index(request):
    return render(request, 'index.html')



def lk(request, id):
    context = {'client': {'name': 'Иван', 'mail': 'Иван@mail.ru', 'password': 'qwerty'}}
    # context = {'client': Client.objects.get(id=id)}
    return render(request, 'lk.html', context=context)


def order(request):
    if request.method == 'POST':
        subscription = []
        for key in request.POST:
            subscription.append({'key': key, 'value': request.POST[key]})
        subscription, created = create_subscription(subscription)
        print(subscription, created)

    allergies = Allergy.objects.all()
    context = []
    for allergy in allergies:
        context.append({'title': allergy.title, 'id': allergy.id})
    return render(request, 'order.html', context={'allergies': context})


def auth(request):
    # input : mail, password
    return render(request, 'auth.html')


def registration(request):
    return render(request, 'registration.html')


def catalog(request):
    context = {}
    return render(request, 'catalog.html', context=context)


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

