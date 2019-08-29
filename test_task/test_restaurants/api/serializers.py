from rest_framework import serializers

from ..models import Restaurant, PreOrder, Reserved


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class PreOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreOrder
        fields = '__all__'


class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserved
        fields = '__all__'
