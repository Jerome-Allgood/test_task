from django.core.exceptions import ValidationError, PermissionDenied
from rest_framework import serializers, request

from ..models import Restaurant, PreOrder, Reserved


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class PreOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreOrder
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        if validated_data['user'] != user:
            raise PermissionDenied
        new_preorder = PreOrder(
            user=validated_data['user'],
            restaurant=validated_data['restaurant']
        )
        new_preorder.save()
        return validated_data


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
            error = {'message': 'No available tables in this restaurant'}
            raise serializers.ValidationError(error)
        return validated_data
