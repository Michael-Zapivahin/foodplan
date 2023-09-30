from django.shortcuts import render, get_object_or_404, redirect

from .forms import ClientForm

from .models import Dish, Allergy, Client, Subscription
from .db_operations import (create_subscription,
                            create_registration,
                            get_authorization,
                            )


def index(request):
    return render(request, 'index.html')


def lk(request, id):
    client = Client.objects.get(id=id)
    subscription = client.subscriptions.filter(status=True).first()
    count = 0
    if subscription.breakfast:
        count += 1
    if subscription.dinner:
        count += 1
    if subscription.desserts:
        count += 1
    if subscription.lunch:
        count += 1
    subscription.count_of_meals = count
    if request.method == "POST":
        form = ClientForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            mail = form.cleaned_data['mail']
            password = form.cleaned_data['password']
            Client.objects.filter(id=id).update(name=name, mail=mail, password=password)

            return redirect('lk', id=client.id)

    else:
        form = ClientForm()
    context = {'form': form, 'client': client, 'subscription': subscription}
    return render(request, 'lk.html', context=context)


def order(request):
    if request.method == 'POST':
        subscription = []
        for key in request.POST:
            subscription.append({'key': key, 'value': request.POST[key]})
        subscription, created = create_subscription(subscription)

    allergies = Allergy.objects.all()
    context = []
    for allergy in allergies:
        context.append({'title': allergy.title, 'id': allergy.id})
    return render(request, 'order.html', context={'allergies': context})


def auth(request):
    authorization, user_id = False, 0
    if request.method == 'POST':
        authorization, user_id = get_authorization(request.POST['email'], request.POST['password'])
    print(authorization, user_id)
    if authorization:
        lk(request, user_id)
    else:
        return render(request, 'auth.html')


def registration(request):
    if request.method == 'POST':
        created, message = create_registration(request.POST)

    return render(request, 'registration.html')


def catalog(request):
    context = {'menu': Dish.objects.all()}
    return render(request, 'catalog.html', context=context)


def card(request, id):
    dish = get_object_or_404(Dish, id=id)
    context = {
        'dish': {
            'title': dish.title,
            'descripion': dish.description,
            'components': dish.components.all(),
            'calories': dish.calories,
            'photo': dish.photo,
        },
    }
    return render(request, 'card.html', context=context)


def sorted_catalog(request, id_):
    subscription = get_object_or_404(Subscription, id=id_)
    menu = Dish.objects.get_menu(subscription)
    context = {'menu': menu}
    return render(request, 'catalog.html', context=context)
