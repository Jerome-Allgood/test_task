from ..models import Restaurant, PreOrder, Reserved
from . import serializers
from rest_framework import generics


class RestaurantListView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer


class RestaurantDetailView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer


class CreatePreorder(generics.CreateAPIView):
    serializer_class = serializers.PreOrderSerializer


class CreateReserve(generics.CreateAPIView):
    serializer_class = serializers.ReserveSerializer

