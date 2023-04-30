from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('seller-index/',views.seller_index,name='seller-index'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('change-password',views.change_password,name='change-password'),
    path('profile/',views.profile,name='profile'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('verify-otp/',views.verify_otp,name='verify-otp'),
    path('New-password/',views.New_password,name='New-password'),
    path('seller-change-password/',views.seller_change_password,name='seller-change-password'),
    path('seller-profile/',views.seller_profile,name='seller-profile'),
    path('seller-add-product/',views.seller_add_product,name='seller-add-product'),
]