from django.apps import AppConfig


class MyAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "my_app"

    def ready(self):
        # Import signal handlers to connect them to their respective signals
        import my_app.signals  # Ensure signals are registered

        print("Signals have been imported and registered.")
