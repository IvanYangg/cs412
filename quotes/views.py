from django.shortcuts import render
from django.templatetags.static import static
import random
# Create your views here.
quotes = [
    "I've always believed that success for anyone is all about drive, dedication, and desire, but for me, it's also been about confidence and faith.",
    "We're going to have to work. We're going to have to play well. Nothing will be given to us.",
    "I always have an optimistic view, no matter what it is.",
    "To excel at the highest level - or any level, really - you need to believe in yourself, and hands down, one of the biggest contributors to my self-confidence has been private coaching.",
    "I'm not in the business of ranking or debating who is what."
]

images = [
    static('pic1.jpg'), 
    static('pic2.webp'),
    static('pic3.webp'),
    static('pic4.jpg'),
]

def quote(request):
    random_quote = random.choice(quotes)
    random_image = random.choice(images)
    return render(request, 'quote.html', {'quote': random_quote, 'image': random_image})

def show_all(request):
    return render(request, 'show_all.html', {'quotes': quotes, 'images': images})

def about(request):
    return render(request, 'about.html')