from django.apps import AppConfig

class AppConfig(AppConfig):
    name = "app"
    verbose_name = "Servicio Empresa"

    def ready(self):
        import app.models  # noqa
