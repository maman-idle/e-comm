from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutView, name='logout'),
    path('main/', views.main, name='mainpage'),
    path('orders/<customer>', views.orders, name='orders'),
    path('product/<product_id>', views.productpage, name='productpage'),
]
