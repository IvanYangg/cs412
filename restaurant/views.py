from django.shortcuts import render
from django.utils import timezone
import random
from datetime import timedelta

# Create your views here.
def main(request):
    return render(request, 'restaurant/main.html')

def order(request):
    special = random.choice(["Steak", "Hot wings", "Smoked Salmon", "Ribs"])
    context = {
        'daily_special': special,
    }
    return render(request, 'restaurant/order.html', context)

def confirmation(request):
    items = request.POST.getlist('items')
    name = request.POST['name']
    phone = request.POST['phone']
    email = request.POST['email']
    prices = {
        'Pizza': 3.0,
        'Burger': 8.0,
        'Fries': 4.0,
        'Salad': 7.0,
        'Daily Special': 20.0
    }

    total_price = sum(prices[item] for item in items)
    ready_time = timezone.now() + timedelta(minutes=random.randint(30, 60))

    context = {
        'items': items,
        'total_price': total_price,
        'customer_name': name,
        'customer_phone': phone,
        'customer_email': email,
        'ready_time': ready_time.strftime('%Y-%m-%d %I:%M %p'),
    }
    return render(request, 'restaurant/confirmation.html', context)