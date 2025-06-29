from rest_framework import serializers
from .models import Catagory, Product, User, CartItem

class CatagorySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    price = serializers.CharField()
    catagory = CatagorySerializer()
    description = serializers.CharField()

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    user = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
class CartItemSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    user = serializers.CharField()
    products= ProductSerializer()
    quantity= serializers.CharField()

    def create(self, validated_data):
        return CartItem.objects.create(**validated_data)