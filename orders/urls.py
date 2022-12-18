from django.urls import path
from . import views

urlpatterns=[
path('',views.order,name='order'),
path('cart/',views.cart,name='cart'),
path('<int:id>',views.remove,name='remove'),
]