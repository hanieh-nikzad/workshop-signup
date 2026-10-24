from django.urls import path

from . import views

urlpatterns = [
    path("w/<int:pk>/", views.workshop_detail, name="workshop_detail"),
    path("r/<uuid:token>/", views.registration_status, name="registration_status"),

]