"""
Root URL configuration for the Codveda Auth System project.

Login, logout, and every password-reset step reuse Django's built-in
`django.contrib.auth.views` classes — we only point them at our own
Bootstrap-styled templates and a couple of custom form classes.
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from accounts.forms import LoginForm

urlpatterns = [
    path("admin/", admin.site.urls),

    # Home page redirects straight into the auth flow.
    path("", auth_views.LoginView.as_view(
        template_name="registration/login.html",
        authentication_form=LoginForm,
    ), name="home"),

    # --- Login / Logout -------------------------------------------------
    path("login/", auth_views.LoginView.as_view(
        template_name="registration/login.html",
        authentication_form=LoginForm,
        redirect_authenticated_user=True,
    ), name="login"),

    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # --- Password reset (4-step flow, all built into Django) ------------
    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset_form.html",
        email_template_name="registration/password_reset_email.html",
        subject_template_name="registration/password_reset_subject.txt",
    ), name="password_reset"),

    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html",
    ), name="password_reset_done"),

    path("password-reset/confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html",
    ), name="password_reset_confirm"),

    path("password-reset/complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html",
    ), name="password_reset_complete"),

    # --- App-specific routes (registration + dashboard) ------------------
    path("accounts/", include("accounts.urls")),
]
