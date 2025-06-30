from rest_framework import serializers
from .models import Catagory, Product, User, CartItem
from attr import fields

class CatagorySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()

    def create(self, validated_data):
        return Catagory.objects.create(**validated_data)

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    price = serializers.CharField()
    catagory = serializers.CharField()
    description = serializers.CharField()

    def create(self, validated_data):
        return Product.objects.create(**validated_data)
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["catagory"] = instance.catagory.name if instance.catagory else None
        return data

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
    products= serializers.CharField()
    quantity= serializers.CharField()

    def create(self, validated_data):
        return CartItem.objects.create(**validated_data)