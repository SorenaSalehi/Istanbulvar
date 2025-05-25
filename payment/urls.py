from django.urls import path

app_name = "payment"


from .views import payment_iframe, zarinpal_callback

urlpatterns = [

    path('payment/zarinpal/<int:order_id>/', payment_iframe, name='payment_zarinpal'),
    path('payment/zarinpal/callback/',       zarinpal_callback, name='zarinpal_callback'),
]
