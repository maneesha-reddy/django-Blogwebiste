
# Create your models here.
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
       Profile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)







@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    #profile = Profile(user=instance)
    instance.profile.save()
post_save.connect(save_profile, sender=User)



