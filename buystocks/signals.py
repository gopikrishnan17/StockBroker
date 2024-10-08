from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Funds

@receiver(post_save, sender=User)
def create_user_funds(sender, instance, created, **kwargs):
    if created:
        # If the user is created, create a Funds object with default balance
        Funds.objects.create(user=instance)
