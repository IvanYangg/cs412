from django.shortcuts import render
import random
# Create your views here.
quotes = [
    "I've always believed that success for anyone is all about drive, dedication, and desire, but for me, it's also been about confidence and faith.",
    "We're going to have to work. We're going to have to play well. Nothing will be given to us.",
    "I always have an optimistic view, no matter what it is."
]

images = [
    'pics/pic1.jpg',
    'pics/pic2.webp',
    'pics/pic3.webp'
]

def quote(request):
    random_quote = random.choice(quotes)
    random_image = random.choice(images)
    return render(request, 'quote.html', {'quote': random_quote, 'image': random_image})
