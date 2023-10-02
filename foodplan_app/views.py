from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

from .forms import ClientForm
from .models import Dish, Allergy, Client, Subscription
from .payment import pay
from .db_operations import (create_subscription,
                            create_registration,
                            get_authorization,
                            get_json_subscription,
                            get_deserialize_subscription,
                            )


def index(request):
    return render(request, 'index.html')


def lk(request):
    if not request.user.is_authenticated:
        return redirect('registration')

    try:
        client = request.user.client.first()
    except Client.DoesNotExist:
        return redirect('auth')
    subscription = get_deserialize_subscription(request.session['subscription'])

    if request.method == "POST":
        form = ClientForm(request.POST, user=request.user)

        if form.is_valid():
            name = form.cleaned_data['name']
            mail = form.cleaned_data['mail']
            password = form.cleaned_data['password']
            Client.objects.filter(user=request.user).update(name=name, mail=mail, password=password)
            user = User.objects.get(
                username=request.user.username,
                email=request.user.email,
                password=request.user.password,
            )
            user.username = name
            user.email = mail
            user.set_password(password)
            user.save()
            return redirect('lk')

    else:
        form = ClientForm(user=request.user)
    context = {'form': form, 'client': client, 'subscription': subscription}
    return render(request, 'lk.html', context=context)


def order(request):
    if request.method == 'POST':

        subscription = []
        for key in request.POST:
            subscription.append({'key': key, 'value': request.POST[key]})

        subscription, created = create_subscription(subscription, request.user)
        if created:
                price = subscription.cost
                phone = '9778107777'
                email = subscription.client.mail
                title = subscription.title
                order_number = subscription.pk

                create_pay = pay(price, phone, email, title, order_number)
                print(create_pay)
                url = create_pay["confirmation"]["confirmation_url"]
                return redirect(url)
        return render(request, 'order.html')

    allergies = Allergy.objects.all()
    context = []
    for allergy in allergies:
        context.append({'title': allergy.title, 'id': allergy.id})
    return render(request, 'order.html', context={'allergies': context})


def auth(request):
    authorization, client_id = False, 0
    if request.method == 'POST':
        authorization, client_id = get_authorization(request, request.POST['email'], request.POST['password'])
    if authorization:
        if 'subscription' in request.session:
            del request.session['subscription']
        client = get_object_or_404(Client, pk=client_id)
        subscription = client.subscriptions.filter(status=True).first()
        json_subscription = get_json_subscription(subscription)
        request.session['subscription'] = json_subscription
        form = ClientForm(request.POST)
        print(client, json_subscription)
        return redirect('lk')
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


def sorted_catalog(request, id):
    subscription = get_object_or_404(Subscription, id=id)
    menu = Dish.objects.get_menu(subscription)
    context = {'menu': menu}
    return render(request, 'catalog.html', context=context)
