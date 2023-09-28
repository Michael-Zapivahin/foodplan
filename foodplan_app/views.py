from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

def card(request):
    return render(request, 'card.html')
