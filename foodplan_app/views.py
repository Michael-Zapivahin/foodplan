from django.shortcuts import render, get_object_or_404, redirect

from .models import Dish, Client
from .forms import ClientForm



def index(request):
    return render(request, 'index.html')



def lk(request, id):
    client = Client.objects.get(id=id)
    if request.method == "POST":
        form = ClientForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            mail = form.cleaned_data['mail']
            password = form.cleaned_data['password']
            Client.objects.filter(id=id).update(name=name, mail=mail, password=password)

            return redirect('lk', id=client.id)

        else:
            print('not valid')
    else:
        form = ClientForm()
    context = {'form': form, 'client': client}
    return render(request, 'lk.html', context=context)


def order(request):
    # context = {'allergies': Allergy.objects.all()}
    context = {
        'allergies': [
            {'title': 'Рыба', 'id': 1},
            {'title': 'Мясо', 'id': 2},
            {'title': 'Сыр', 'id': 3},
        ],
    }
    return render(request, 'order.html', context=context)


def auth(request):
    # input : mail, password
    return render(request, 'auth.html')


def registration(request):
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

