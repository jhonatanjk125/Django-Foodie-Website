from django.urls import path
from . import views


urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('<slug:vendor_slug>/', views.vendorPage, name='vendorPage'),

    #Add to cart
    path('add_to_cart/<int:product_id>/', views.addToCart, name='addToCart')

]