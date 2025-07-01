from django.urls import path
from .views import ProductList, UserRegister, UserLogin, CatagoryList, CartList, OrderItem, UserAddressView, MakePayment

urlpatterns = [
    path('products/', ProductList.as_view()),
    path('user/register/', UserRegister.as_view()),
    path('user/login/', UserLogin.as_view()),
    path('catagory/', CatagoryList.as_view()),
    path('cart/', CartList.as_view()),
    path('user/address/', UserAddressView.as_view()),
    path('cart/order/', OrderItem.as_view()),
    path('cart/payment/', MakePayment.as_view()),
]
