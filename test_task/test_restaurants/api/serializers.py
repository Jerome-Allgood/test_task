from django.core.exceptions import ValidationError
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
    # pre_order = PreOrderSerializer(read_only=True)

    class Meta:
        model = Reserved
        fields = (
            'id',
            'creation_date',
            'preorder',
            'comment',
        )

    def create(self, validated_data):
        restaurant = validated_data['preorder'].restaurant
        reserves = Reserved.objects.filter(preorder__restaurant=restaurant)
        if reserves.count() < restaurant.tables:
            new_reserve = Reserved(
                preorder=validated_data['preorder'],
                comment=validated_data['comment']
            )
            new_reserve.save()
            pre_order = validated_data['preorder']
            pre_order.status = 'confirmed'
            pre_order.save()
        else:
            raise ValidationError('No available tables')
        return validated_data
