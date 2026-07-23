"""
Views for the accounts app.

Login, logout, and all password-reset steps are handled entirely by
Django's built-in `django.contrib.auth.views` (wired up in
config/urls.py) — that code is security-reviewed by the Django team,
so we don't reinvent it. This module only adds the two pieces Django
doesn't ship out of the box: registration and the post-login
dashboard.
"""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import RegistrationForm
from .models import Profile


def register_view(request):
    """Create a new account and log the user straight in."""
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f"Welcome aboard, {user.first_name or user.username}! Your account was created successfully.",
            )
            return redirect("dashboard")
        messages.error(request, "Please fix the errors below and try again.")
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard_view(request):
    """
    Landing page after login.

    Shows different content depending on the signed-in user's role:
    admins see account/user-management stats, regular users see a
    simpler personal summary.
    """
    profile, _ = Profile.objects.get_or_create(user=request.user)

    context = {"profile": profile}

    if profile.is_admin:
        from django.contrib.auth.models import User
        context["total_users"] = User.objects.count()
        context["admin_count"] = Profile.objects.filter(role=Profile.Role.ADMIN).count()
        context["recent_users"] = User.objects.order_by("-date_joined")[:5]

    return render(request, "accounts/dashboard.html", context)
