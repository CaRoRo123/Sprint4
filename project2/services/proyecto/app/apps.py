from django.apps import AppConfig


class AppConfig(AppConfig):
    name = "app"
    verbose_name = "Servicio Proyecto"

    def ready(self):
        # Registrar señales al iniciar Django
        import app.models  # noqa: F401
