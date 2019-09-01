from ..models import Restaurant, PreOrder, Reserved
from . import serializers
from rest_framework import generics


class RestaurantListView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer


class RestaurantDetailView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer


class Preorders(generics.ListCreateAPIView):
    queryset = PreOrder.objects.all()
    serializer_class = serializers.PreOrderSerializer


class Reserves(generics.ListCreateAPIView):
    queryset = Reserved.objects.all()
    serializer_class = serializers.ReserveSerializer
