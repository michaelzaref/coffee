from django.urls import path
from . import views

urlpatterns = [
    path('signin',views.signin, name='signin'),
    path('signup',views.signup, name='signup'),
    path('profile',views.profile , name='profile'),
    path('logout', views.logout, name='logout'),
    path('favorite/<int:pro_id>',views.favorite,name='favorite'),
    path('fav',views.show_fav,name='fav')
]