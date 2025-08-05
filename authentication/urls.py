from django.urls import path
from . import views

urlpatterns =[
path('',views.store,name='store'),
path('cart/',views.cart,name='cart'),
path('checkout/',views.checkout,name='checkout'),
path('update_item/',views.update_item, name='update_item'),
path('signup/',views.signup, name='signup'),
path('signin/',views.signin, name='signin'),
path('signout/',views.signout, name='signout'),
path('user_dashboard/',views.user_dashboard, name='user_dashboard'),
]