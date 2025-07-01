from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Catagory, Product, User, AuthToken, CartItem, UserAddress
from .serializers import CatagorySerializer, ProductSerializer, UserSerializer, CartItemSerializer, OrderItemSerializer, UserAddressSerializer
from api.utils.utils import hash_password, check_password, OrderStatus
from api.model.request_models import UserLoginRequest, CartListRequest
from api.model.request_models import Product as ProductRequest
from api.authentication.auth import auth_wrapper
from api.logging.logging import logger


class UserRegister(APIView):
    def post(self, request, format=None):
        input_data: dict = request.data
        user = User.objects(user=input_data["user"]).first()
        if user:
            return Response({"error": "User already exists"}, status=400)
        input_data["password"] = hash_password(input_data.pop("password"))
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class UserLogin(APIView):
    def post(self, request):
        print(request.data)
        user_data = UserLoginRequest.from_dict(request.data)
        user = User.objects(user=user_data.user).first()
        if user and check_password(user_data.password, user.password):
            auth_token = AuthToken.objects(user=user.id).first()
            if not auth_token or not auth_token.is_valid():
                if auth_token:
                    auth_token.delete()
                auth_token = AuthToken(user=str(user.id))
                auth_token.save()
                return Response({"token": auth_token.token}, status=200)
            return Response({"token": auth_token.token}, status=200)
        return Response({"errors": "Incorrect password"}, status=400)


class UserAddressView(APIView):
    @auth_wrapper
    def post(self, request):
        request.data["user"] = str(request.user.id)
        address = UserAddress.objects(user=request.user.id).first()
        print(address.get_address())
        if address:
            return Response({"errors": "Address Already exists for this user"}, status=400)
        serializer = UserAddressSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class CatagoryList(APIView):

    @auth_wrapper
    def get(self, request):
        categorys = Catagory.objects.all()
        if categorys:
            serializer = CatagorySerializer(categorys, many=True)
            return Response(serializer.data, status=200)
        return Response({"errors": "Categories not found"}, status=400)

    @auth_wrapper
    def post(self, request):
        seralizer = CatagorySerializer(data=request.data)
        if seralizer.is_valid():
            seralizer.save()
            return Response(seralizer.data, status=200)
        return Response(seralizer.errors, status=400)
    

class ProductList(APIView):

    @auth_wrapper
    def get(self, request):
        products = Product.objects.all()
        if products:
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=200)
        return Response({"errors": "Products not found"}, status=400)
    
    @auth_wrapper
    def post(self, request):
        product_request = ProductRequest.from_dict(request.data)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            catagory = Catagory.objects(id=product_request.catagory).first()
            if not catagory:
                return Response({"errors": "Category not found"}, status=400)
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CartList(APIView):

    @auth_wrapper
    def get(self, request):
        user_id = request.user.id
        print(user_id)
        product_list = CartItem.objects(user=user_id)
        if product_list:
            serializer = CartItemSerializer(product_list, many=True)
            return Response(serializer.data, status=200)
        return Response({"errors": "Cart item for this particulaor user is empty"}, status=400)

    @auth_wrapper
    def post(self, request):
        logger.info("Cart list post func called..")
        input_data = CartListRequest.from_dict(request.data)
        input_data.user = str(request.user.id)
        serializer = CartItemSerializer(data= input_data.to_dict())
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class OrderItem(APIView):

    @auth_wrapper
    def get(self, request):
        user_id = request.user.id
        user_address = UserAddress.objects(user=user_id).first()
        print(user_address.get_address())
        # if user_address:
        product_details = Product.objects(user=user_id)
        for product_detail in product_details:
            print(product_detail)


    @auth_wrapper
    def post(self, request):
        user_id = request.user.id
        cart_items = CartItem.objects(user=user_id)
        cart_ids = []
        if cart_items:
            for cart in cart_items:
                cart_ids.append(cart.id)
            order = OrderItem(user=user_id, cart_items=cart_ids, order_status=OrderStatus.in_progress)
            order.save()
            return Response(order, status=200)
        return Response({"errors": "Cart is empty"}, status=400)


class MakePayment(APIView):
    pass
