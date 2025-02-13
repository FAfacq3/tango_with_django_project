from django.urls import path
from rango import views
from django.contrib.auth import views as auth_views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path("about/", views.about, name="about"),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='rango/login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<category_name_slug>/add_page/', views.add_page, name='add_page'),
    path("like_category/", views.like_category, name="like_category"),
    path('category/<slug:category_slug>/', views.show_category, name='show_category'),
    path('page/<int:page_id>/', views.show_page, name='show_page'),
    path('search/', views.search, name='search'),
    path('restricted/', views.restricted, name='restricted'),
]
