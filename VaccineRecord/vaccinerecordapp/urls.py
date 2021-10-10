from django.urls import path 
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('search-create-patient/', views.search_create_patient, name="search-create-patient"),
    path('create-patient/', views.create_patient, name="create-patient"),
    path('tool/', views.tool, name="tool"),

]