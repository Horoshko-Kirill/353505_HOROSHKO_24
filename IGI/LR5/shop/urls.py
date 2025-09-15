from django.urls import path
from django.urls import re_path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('careers/', views.careers, name='careers'),
    path('client_orders/', views.client_orders, name='client_orders'),
    path('contacts/', views.contacts, name='contacts'),
    path('coupons/', views.coupons, name='coupons'),
    path('employee_orders/', views.employee_orders, name='employee_orders'),
    path('faq/', views.faq, name='faq'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('auth-options/', views.auth_options, name='auth_options'),
    path('manufacturers/', views.manufacturers, name='manufacturers'),
    path('news/', views.news, name='news'),
    path('privacy/', views.privacy, name='privacy'),
    path('register/client/', views.register_client, name='register_client'),
    path('register/employee/', views.register_employee, name='register_employee'),
    re_path(r'^product_charts/$', views.product_charts, name='product_charts'),
    re_path(r'^products/$', views.products, name='products'),
    re_path(r'^reviews/$', views.reviews, name='reviews'),

    path('manufacturers/add/', views.add_manufacturer, name='add_manufacturer'),
    path('manufacturers/add/', views.add_manufacturer, name='add_manufacturer'),
    path('manufacturers/edit/<int:pk>/', views.edit_manufacturer, name='edit_manufacturer'),
    path('manufacturers/delete/<int:pk>/', views.delete_manufacturer, name='delete_manufacturer'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('reviews/add/', views.add_review, name='add_review'),
    path('add_to_order/<int:product_id>/', views.add_to_order, name='add_to_order'),
    path('current_order/', views.current_order, name='current_order'),
    path('remove_from_order/<int:item_id>/', views.remove_from_order, name='remove_from_order'),
    path('confirm_order/<int:order_id>/', views.confirm_order, name='confirm_order'),
]