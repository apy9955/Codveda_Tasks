"""Admin-site registration for the accounts app."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    """Lets an admin edit the role directly on the User edit page."""
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = BaseUserAdmin.list_display + ("get_role",)

    @admin.display(description="Role")
    def get_role(self, obj):
        return obj.profile.get_role_display() if hasattr(obj, "profile") else "—"


# Re-register User with the Profile inline attached.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Profile)

admin.site.site_header = "Codveda Auth System Administration"
admin.site.site_title = "Codveda Auth System"
admin.site.index_title = "Site Administration"
