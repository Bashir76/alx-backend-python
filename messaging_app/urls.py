from django.urls import path, include

urlpatterns = [
    path("api/", include("messaging_app.chats.urls")),
]
