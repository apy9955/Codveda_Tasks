from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        # Import signal handlers so the post_save receiver in
        # models.py gets registered when the app loads.
        import accounts.models  # noqa: F401
