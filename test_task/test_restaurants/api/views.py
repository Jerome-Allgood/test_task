from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import authentication_classes, \
    permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

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

    def post(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return Response({'error': 'Not authorized'})
        return self.create(request, *args, **kwargs)


class Reserves(generics.ListCreateAPIView):
    queryset = Reserved.objects.all()
    serializer_class = serializers.ReserveSerializer
    permission_classes = [IsAdminUser]
