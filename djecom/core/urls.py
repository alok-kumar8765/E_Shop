from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static
from core.views import index, signup, Signup, Login, Index, cart, CheckOut ,logout #Login is for class and login is for function

urlpatterns = [
    #path('',index,name='homepage'),
    path('',Index.as_view(),name='homepage'),
    #path('signup',signup),
    #path('login',login),
    path('login',Login.as_view(),name='login'),
    path('signup',Signup.as_view(),name='signup'),
    path('logout',logout,name='logout'),
    path('cart',cart.as_view(),name='cart'),
    path('check-out',CheckOut.as_view(),name='checkout'),
    #path('order',order.as_view(),name='order'),
]
