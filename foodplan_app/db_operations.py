from random import choice

from .models import Subscription, Allergy, Client, Menu, SubscriptionAllergy, Dish

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.serializers import serialize, deserialize


def get_authorization(request, email, password):
    clients = Client.objects.filter(mail=email)
    if clients:
        client = clients[0]
    else:
        return False, 0

    user = authenticate(username=client.name, password=password)
    if user is not None:
        login(request, user)

    if user is not None:
        return True, client.pk
    else:
        return False, 0


def create_subscription(subscription, user):
    cost_per_month = 100
    terms = {
        '0': 1,
        '1': 3,
        '2': 6,
        '3': 12,
    }
    breakfast = False
    lunch = False
    dinner = False
    dessert = False
    persons = 1
    term = 1
    allergies = []
    description = ''
    for item in subscription:
        key = item['key']
        if key == 'select0':
            term = terms.get(item['value'])
            description=f'Subscription for {term} months'
        elif key == 'select1' and item['value'] == '0':
            breakfast = True
            description += ', breakfast'
        elif key == 'select2' and item['value'] == '0':
            lunch = True
            description += ', lunch'
        elif key == 'select3' and item['value'] == '0':
            dinner = True
            description += ', dinner'
        elif key == 'select4' and item['value'] == '0':
            dessert = True
            description += ', dessert'
        elif key == 'select5':
            persons = int(item['value']) + 1
            description += f' for {persons} persons'
        elif key.find('allergy') >= 0:
            values = key.split('_')
            allergies.append(values[1])

    clients = Client.objects.filter(user=user)
    if clients:
        client = clients[0]

    subscription, created = Subscription.objects.get_or_create(
        title=f'Subscription for {term} months',
        description=description,
        term=term,
        breakfast=breakfast,
        lunch=lunch,
        dinner=dinner,
        desserts=dessert,
        persons_number=persons,
        cost=cost_per_month * term,
        client=client,
    )

    for allergy_id in allergies:
        allergies = Allergy.objects.filter(pk=int(allergy_id))
        if clients:
            allergy = allergies[0]
        SubscriptionAllergy.objects.get_or_create(subscription=subscription, allergy=allergy)
    return subscription, created


def create_registration(registration):
    if registration['password'] == registration['confirmation']:
        user = User.objects.create_user(registration['name'], registration['email'], registration['password'])
        client, created = Client.objects.get_or_create(
            name=registration['name'],
            mail=registration['email'],
            login=registration['name'],
            password='',
            user=user,
        )
        return created, "The user successfully created"
    else:
        return False, f'Wrong password {registration["email"]}, retry input'


def get_json_subscription(subscription):
    if not subscription:
        return None
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
    json_subscription = serialize('json', [subscription])
    return json_subscription


def get_deserialize_subscription(session_json_subscription):
    if session_json_subscription:
        for obj in deserialize('json', session_json_subscription):
            subscription = obj.object
            return subscription
    return None


def delete_subscription(subscription):
    Subscription.objects.filter(id=subscription.id).delete()


def get_week_menu(subscription):
    menu = Dish.objects.get_menu(subscription)
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    week = []
    breakfasts = []
    lunches = []
    desserts = []
    dinners = []
    breakfast = None
    lunch = None
    dessert = None
    dinner = None

    if subscription.breakfast:
        breakfasts = menu.filter(tags__tag__title='Завтрак')
    if subscription.lunch:
        lunches = menu.filter(tags__tag__title='Обед')
    if subscription.desserts:
        desserts = menu.filter(tags__tag__title='Ужин')
    if subscription.dinner:
        dinners = menu.filter(tags__tag__title='Десерт')

    choice_breakfasts = breakfasts
    choice_lunches = lunches
    choice_desserts = desserts
    choice_dinners = dinners

    for day in days:
        if choice_breakfasts:
            try:
                breakfast = choice(choice_breakfasts)
            except IndexError:
                choice_breakfasts = breakfasts
                breakfast = choice(choice_breakfasts)
        if choice_lunches:
            try:
                lunch = choice(choice_lunches)
            except IndexError:
                choice_lunches = lunches
                lunch = choice(choice_lunches)
        if choice_desserts:
            try:
                dessert = choice(choice_desserts)
            except IndexError:
                choice_desserts = desserts
                dessert = choice(choice_desserts)
        if choice_dinners:
            try:
                dinner = choice(choice_dinners)
            except IndexError:
                choice_desserts = desserts
                dinner = choice(choice_dinners)

        dayle_menu = {
            'title': day,
            'breakfast': breakfast,
            'lunch': lunch,
            'dessert': dessert,
            'dinner': dinner,
        }
        week.append(dayle_menu)

    return week

