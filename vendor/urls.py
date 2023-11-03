from django.urls import include, path
from . import views
from accounts import views as accounts_views


urlpatterns = [
    path('', accounts_views.myAccount),
    path('profile/', views.vendorProfile, name='vendorProfile'),
    path('menuBuilder/', views.menuBuilder, name='menuBuilder'),
    path('menuBuilder/category/<int:pk>', views.categories, name='categories'),

    #CRUD Operations
    path('menuBuilder/category/add/', views.addCategory, name='addCategory'),
    path('menuBuilder/category/edit/<int:pk>/', views.editCategory, name='editCategory'),
    path('menuBuilder/category/delete/<int:pk>/', views.deleteCategory, name='deleteCategory'),
]