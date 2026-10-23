from django.urls import path

from . import views

urlpatterns = [
    path("w/<int:pk>/", views.workshop_detail, name="workshop_detail"),
]