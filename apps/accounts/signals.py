# apps/accounts/signals.py

"""
Signal handlers for accounts application.
"""

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
import os

User = get_user_model()


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        # Perform actions for newly created users
        # For example, create related models or send welcome email
        pass


@receiver(pre_delete, sender=User)
def user_pre_delete(sender, instance, **kwargs):
    # Delete avatar file if it exists
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)