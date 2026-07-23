"""
Models for the accounts app.

We deliberately avoid a custom User model (which is hard to change
mid-project) and instead extend Django's built-in `User` with a
one-to-one `Profile` model. This keeps `django.contrib.auth`
(login, logout, password reset, admin, permissions, ...) working out
of the box while still letting us store a "role" for each account.
"""

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """Extra, app-specific data attached to every Django User."""

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        USER = "user", "User"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
        help_text="Controls what the user can see/do on the dashboard.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Keep every User in sync with a Profile.

    - On first creation of a User, automatically create a matching
      Profile (Django superusers created via `createsuperuser` are
      automatically given the "admin" role).
    - On later saves, just persist the existing profile so `save()`
      calls on the User don't error out if a Profile already exists.
    """
    if created:
        Profile.objects.create(
            user=instance,
            role=Profile.Role.ADMIN if instance.is_superuser else Profile.Role.USER,
        )
    else:
        # Guard against legacy users created before this signal existed.
        Profile.objects.get_or_create(user=instance)
        instance.profile.save()
