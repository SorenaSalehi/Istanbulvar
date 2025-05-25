from .views import (
    httpSignup,
    httpVerifyCode,
    httpLoginView,
    httpLogout,
    httpLoginByCode,
    httpAddAddress,
    set_current_address,
    delete_address
)
from django.urls import path


# app_name = "users"

urlpatterns = [
    path("signup/", httpSignup, name="signup"),
    path("login/", httpLoginView, name="login"),
    path("add_new_address/",httpAddAddress,name="addNewAddress"),
    path("logout/", httpLogout, name="logout"),
    path("login_by_code/", httpLoginByCode, name="loginByCode"),
    path("verify_code/", httpVerifyCode, name="verifyCode"),
    path("set_current_address/", set_current_address, name="setCurrentAddress"),
    path('delete_address/', delete_address, name='deleteAddress'),
]
