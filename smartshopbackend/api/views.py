from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Catagory, Product, User, AuthToken
from .serializers import CatagorySerializer, ProductSerializer, UserSerializer, CartItemSerializer
from api.utils.utils import hash_password, check_password
from api.model.request_models import UserLoginRequest, CartListRequest
from api.authentication.auth import auth_wrapper
from api.logging.logging import logger


class UserRegister(APIView):
    def post(self, request, format=None):
        print(request.data)
        input_data: dict = request.data
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


class CatagoryList(APIView):

    @auth_wrapper
    def get(self, request):
        catagorys = Catagory.objects.all()
        if catagorys:
            serializer = CatagorySerializer(data=catagorys, many=True)
            return Response(serializer.data, status=200)
        return Response({"errors": "Catagory not found"}, status=400)

    @auth_wrapper
    def post(self, request):
        seralizer = CatagorySerializer(data=request.data)
        if seralizer.is_valid():
            seralizer.save()
            return Response(seralizer.data, status=200)
        return Response(seralizer.errors, status=400)
    

class ProductList(APIView):

    @auth_wrapper
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    @auth_wrapper
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            catagory = Catagory.objects(catagory=request.data.get("catagory")).first()
            if not catagory:
                return Response({"errors": "Catagory not found"}, status=400)
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CartList(APIView):

    @auth_wrapper
    def get(self):
        pass

    @auth_wrapper
    def post(self, request):
        logger.info("Cart list post func called..")
        input_data = CartListRequest.from_dict(request.data)
        user_id = "request.user.id"
        request.data.update({'user': user_id})
        serializer = CartItemSerializer(data= request.data)
        if serializer.is_valid():
            total_price = input_data.quantity * input_data.products.price
            print(total_price)
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)





        
