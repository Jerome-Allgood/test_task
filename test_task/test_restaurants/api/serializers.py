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
    class Meta:
        model = Reserved
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        r = Restaurant.objects.get(preorder__reserved=1)
        print(r)
        reserves = Reserved.objects.filter(
            restaurant=validated_data['restaurant']).filter(
            preorder=validated_data['preorder'])
        if not reserves:
            pre_order = validated_data['preorder']
            reserve = Reserved(
                user=validated_data['user'],
                restaurant=validated_data['restaurant'],
                preorder=pre_order,
                comment=validated_data['comment']
            )
            reserve.save()
            pre_order.status = 'confirmed'
            pre_order.save()
            return validated_data
        else:
            raise ValidationError('Such reserve already exist')
