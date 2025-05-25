from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.contrib import messages
from dotenv import load_dotenv
from shop.models import Cart, Order
from .models import PaymentLog
import requests
import os

load_dotenv()
User = get_user_model()

ZP_MERCHANT_ID       = os.getenv("ZP_MERCHANT_ID")
ZP_REQUEST_URL       = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_START_PAY_URL     = "https://www.zarinpal.com/pg/StartPay/"
ZP_VERIFY_URL        = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_CALLBACK_PATH     = "/payment/zarinpal/callback/"


if not ZP_MERCHANT_ID:
    raise ValueError("Cannot load ZP_MERCHANT_ID from environment!")


def payment_iframe(request, order):
    # 1. آماده‌سازی مبلغ (تومان → ریال)
    amount_riyal = int(order.total_price) * 10

    # 2. درخواست Authority
    payload = {
        "merchant_id": ZP_MERCHANT_ID,
        "amount": amount_riyal,
        "callback_url": request.build_absolute_uri("/payment/callback/"),
        "description": f"پرداخت سفارش #{order.id}",
    }
    res = requests.post(
        ZP_REQUEST_URL,
        json=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    result = res.json().get("data", {})

    if result.get("code") != 100:
        # لاگ خطا و برگشت به سبد
        PaymentLog.objects.create(orderId=order.id, log=f"ZP Request Error: {res.text}")
        return redirect("shop:checkOut")

    authority = result["authority"]
    PaymentLog.objects.create(orderId=order.id, log=f"ZP Authority: {authority}")

    gateway_url = f"{ZP_START_PAY_URL}{authority}"
    context = {
        "gateway_url": gateway_url,
        "params": {}  
    }
    return render(request, "BankPayment.html", context)


@csrf_exempt
def zarinpal_callback(request):
    """
    این ویو توسط زرین‌پال GET می‌شود با پارامترهای Authority و Status
    """
    authority = request.GET.get("Authority")
    status    = request.GET.get("Status")

    order_id      = request.session.get("zarinpal_order_id")
    amount_riyal  = request.session.get("zarinpal_amount_riyal")

    # اگر سشن نداشته باشیم، خطا می‌زنیم
    if not order_id or not amount_riyal:
        messages.error(request, "اطلاعات پرداخت یافت نشد.")
        return redirect("/")

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        PaymentLog.objects.create(
            orderId=order_id,
            log="زنجیره سشن پاک شده؛ سفارش پیدا نشد."
        )
        messages.error(request, "سفارش شما یافت نشد.")
        return redirect("/")

    # اگر پرداخت کنسل شده باشه
    if status != "OK":
        PaymentLog.objects.create(
            orderId=order_id,
            log=f"Payment Canceled or Failed by User – Status: {status}, Authority: {authority}"
        )
        messages.error(request, "پرداخت کنسل شد یا با خطا مواجه شد.")
        return redirect("/")

    # تأیید پرداخت
    verify_payload = {
        "merchant_id": ZP_MERCHANT_ID,
        "authority": authority,
        "amount": amount_riyal,
    }
    verify_res = requests.post(ZP_VERIFY_URL, json=verify_payload)
    verify_data = verify_res.json().get("data", {})

    if verify_data.get("code") == 100:
        # موفقیت‌آمیز
        ref_id = verify_data.get("ref_id")
        order.status = "paid"
        order.save()

        # خالی کردن سبد
        cart = get_or_create_cart(request)
        for item in cart.items.all():
            item.delete()
        if cart.items.count() == 0:
            cart.delete()

        # لاگ پرداخت موفق
        PaymentLog.objects.create(
            orderId=order_id,
            log=f"Payment Verified – RefID: {ref_id}"
        )

        # ارسال SMS به ادمین‌ها
        admin_numbers = [u.phone_number for u in User.objects.filter(is_staff=True) if u.phone_number]
        if admin_numbers:
            newOrderSMS(order_id, admin_numbers)

        messages.success(request, "پرداخت با موفقیت انجام شد!")
        return redirect("/")
    else:
        PaymentLog.objects.create(
            orderId=order_id,
            log=f"Verification Failed – {verify_res.json()}"
        )
        messages.error(request, "خطا در تأیید پرداخت. لطفاً با پشتیبانی تماس بگیرید.")
        return redirect("/")


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    cart_id = request.session.get("cart_id")
    if cart_id:
        try:
            return Cart.objects.get(pk=cart_id, user__isnull=True)
        except Cart.DoesNotExist:
            pass
    new_cart = Cart.objects.create()
    request.session["cart_id"] = new_cart.id
    return new_cart


def newOrderSMS(orderId: int | str, numbers: list[str]):
   print("پرداخت انجام شد ولی بعدا اس ام اس رو هم فعال کن")
