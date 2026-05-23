from django.urls import path, include

urlpatterns = [
    path("api/areas/", include("app.urls")),
]
