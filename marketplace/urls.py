from django.urls import path
from . import views


urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('<slug:vendor_slug>/', views.vendorPage, name='vendorPage'),

    #Add to cart
    path('add_to_cart/<int:product_id>/', views.addToCart, name='addToCart'),
    #Remove from cart
    path('remove_from_cart/<int:product_id>/', views.removeFromCart, name='removeFromCart'),
    #Delete cart
    path('delete_cart/<int:product_id>', views.deleteCart, name='deleteCart'),

]