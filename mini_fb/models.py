from django.db import models

# Create your models here.
class Profile(models.Model):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=100, blank=False)
    email = models.EmailField(blank=False)
    profile_image_url = models.URLField(max_length=255)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'