# Name: Ivan Yang
# BU Email: yangi@bu.edu
# Description: This file defines all the custom models and their data attributes that is used in this project

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
# a custom profile model that defines the first_name, last_name, city, email, and profile_image_url data attributes of a generic user. 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=100, blank=False)
    email = models.EmailField(blank=False)
    profile_image_url = models.URLField(max_length=255)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        return StatusMessage.objects.filter(profile=self).order_by('-timestamp')
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_friends(self):
        friends1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
        friends2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)
        return Profile.objects.filter(id__in=list(friends1) + list(friends2))

# a custom profile model that defines status messages that are linked to a profile. Has data attributes, timestamp, message, and profile, which is the foreign key. 
class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profile.first_name} - {self.message}"
    
    def get_images(self):
        return Image.objects.filter(status_message=self)
    
# a custom image model for adding and storing images into the database
class Image(models.Model):
    image_file = models.ImageField(blank=True) 
    status_message = models.ForeignKey('StatusMessage', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

# a custom model for friends functionality
class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, related_name="profile1", on_delete=models.CASCADE)
    profile2 = models.ForeignKey(Profile, related_name="profile2", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.profile1.user.username} & {self.profile2.user.username}"