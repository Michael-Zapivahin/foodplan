from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def card(request, id=None):
    return render(request, 'card.html')


def lk(request, id):
    context = {'client': {'name': 'Иван', 'mail': 'Иван@mail.ru', 'password': 'qwerty'}}
    # context = {'client': Client.objects.get(id=id)}
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
    context = {}
    return render(request, 'catalog.html', context=context)

