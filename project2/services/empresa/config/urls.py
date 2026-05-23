from django.urls import path, include

urlpatterns = [
    path("api/empresas/", include("app.urls")),
]
