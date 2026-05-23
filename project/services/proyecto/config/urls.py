from django.urls import path, include

urlpatterns = [
    path("api/proyectos/", include("app.urls")),
]
