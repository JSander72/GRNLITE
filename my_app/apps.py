from django.apps import AppConfig


# class GrnliteConfig(AppConfig):
#     default_auto_field = "django.db.models.BigAutoField"
#     name = "grnlite"

#     def ready(self):
#         import grnlite.signals


class MyAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "my_app"

    def ready(self):
        import my_app.signals
