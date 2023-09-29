from .models import Subscription, Allergy, Client, Menu

from django.shortcuts import get_object_or_404


def create_subscription(subscription):
    cost_per_month = 100
    client = get_object_or_404(Client, pk=1)
    menu = get_object_or_404(Menu, pk=1)
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
    print(subscription)
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
        elif key.find('allergy_') > 0:
            try:
                allergy_id = key.split('_')[1]
            except:
                print(f'error {key}')
                allergy_id = 1
            allergies.append(get_object_or_404(Allergy, pk=allergy_id))

    print(breakfast, lunch, dinner, dessert, description)

    subscription, created = Subscription.objects.get_or_create(
        title=f'Subscription for {term} months',
        description=description,
        term=term,
        breakfast=breakfast,
        lunch=lunch,
        dinner=dinner,
        desserts=dessert,
        persons_number=persons,
        # allergy=allergy,
        cost=cost_per_month * term,
        client=client,
        menu=menu
    )
    return subscription, created

