from django.urls import path

from . import views

urlpatterns = [
    path("w/<int:pk>/", views.workshop_detail, name="workshop_detail"),
    path("r/<uuid:token>/", views.registration_status, name="registration_status"),
    path("r/<uuid:token>/cancel/", views.cancel_registration, name="cancel_registration"),
    path("", views.home, name="home"),
    path("m/<uuid:token>/", views.workshop_manage, name="workshop_manage"),

]