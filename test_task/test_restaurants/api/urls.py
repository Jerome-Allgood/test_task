from django.urls import path

from . import views

urlpatterns = [
    path('restaurants/', views.RestaurantListView.as_view()),
    path('restaurants/<int:pk>/', views.RestaurantDetailView.as_view()),
    path('preorders/', views.Preorders.as_view()),
    path('reserves/', views.Reserves.as_view()),


]
