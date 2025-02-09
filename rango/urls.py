from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_page/', views.add_page, name='add_page'),
    path('like_category/', views.like_category, name='like_category'),
    path('category/<str:category_name>/', views.show_category, name='show_category'),
    path('page/<int:page_id>/', views.show_page, name='show_page'),
    path('search/', views.search, name='search'),
]
