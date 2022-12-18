from django.urls import path
from django.urls.resolvers import URLPattern
from . import views


urlpatterns=[

    path('',views.products,name='products'),
    path('<int:pro_id>',views.product,name='product'),
    path('search',views.search,name='search'),

]