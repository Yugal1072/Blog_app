
from django.urls import path
from blogapp.views import *

urlpatterns = [
    path('', base, name='base'),
    path('homepage/', homepage, name='homepage'),
    path('signup_page/', signup_page, name='signup_page'),
    path('login_page/', login_page, name='login_page'),
    path('logout_page/', logout_page, name='logout_page'),
    path('add_blogs/', add_blogs, name='add_blogs'),
]


