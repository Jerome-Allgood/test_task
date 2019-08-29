from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home-view'),
    path('restaurants/<int:pk>', views.RestaurantDetailView.as_view(),
         name='restaurant-detail'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/my-orders/', views.MyOrders.as_view(), name='my-orders'),
    path('preorders/', views.AllOrders.as_view(), name='all-orders'),
    path('reserves/', views.AllReserves.as_view(), name='all-reserves'),
    path('create-preorder/', views.CreatePreorder.as_view(), name='create-preorder'),


]
