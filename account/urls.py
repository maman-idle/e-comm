from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutView, name='logout'),
    path('main/', views.main, name='mainpage'),
    path('orders/<customer>', views.orders, name='orders'),
    path('delete-order/<order_id>', views.delete_order, name='delete_order'),
    path('edit-profile/<customer_id>', views.edit_profile, name='edit_profile'),
    path('product/<product_id>', views.productpage, name='productpage'),
    path('about/', views.about, name='about'),
    path('staff/', views.staff_page, name='staff_page'),
    path('deliver/<order_id>', views.deliver, name='deliver'),
    path('cancel-delivery/<order_id>', views.cancel_delivery, name='cancel'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<product_id>', views.edit_product, name='edit_product'),
    path('delete-product/<product_id>',
         views.delete_product, name='delete_product')
]
