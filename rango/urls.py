from django.urls import path, include
from . import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('myview/', views.my_view, name='my_view'),
    path('greet/', views.greeting_view, name='greet'),
    path('categories/', views.show_categories, name='show_categories'),
    path('category/<slug:category_name_slug>/', views.category, name='category'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
]
