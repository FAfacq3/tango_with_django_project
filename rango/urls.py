from django.urls import path
from . import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('myview/', views.my_view, name='my_view'),
]
