from .forms import VerifyCodeForm, SignUpForm, LoginForm, LoginByCodeForm, AddressForm
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib import messages
from .models import Code, Address
from django.http import JsonResponse
from django.conf import settings
import json


User = get_user_model()


def httpSignup(request):
    redirect_url = request.POST.get("next", "/")
    if request.user.is_authenticated:
        return JsonResponse(
            {
                "status": "redirect",
                "redirect_url": redirect_url,
            }
        )

    if request.method == "POST":
        user = None

        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            phoneNumber = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            user = (
                User.objects.filter(email=email).first()
                or User.objects.filter(phone_number=phoneNumber).first()
            )

            if user:
                if user.is_phone_verified:
                    messages.info(request, "شما قبلاً حساب فعالی دارید.")
                    return redirect(f"{reverse('login')}?next={redirect_url}")
                else:
                    messages.error(
                        request,
                        "حساب شما فعال نیست. لطفاً شماره تلفن خود را تأیید کنید.",
                    )
                    user.code.save()
            else:
                user = User(
                    username=phoneNumber,
                    email=email,
                    phone_number=phoneNumber,
                )
                user.set_password(password)
                user.save()
            if user:
                request.session["user_id"] = user.id
                return redirect(f"{reverse('verifyCode')}?next={redirect_url}")

        else:
            for _, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    return JsonResponse(
        {
            "status": "redirect",
            "redirect_url": redirect_url,
        }
    )


def httpLoginView(request):
    redirect_url = request.POST.get("next", "/")
    if request.user.is_authenticated:
        return JsonResponse(
            {
                "status": "redirect",
                "redirect_url": redirect_url,
            }
        )

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():

            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            user = authenticate(username=phone_number, password=password)
            if user is not None:
                if user.is_phone_verified:
                    login(request, user)
                    messages.success(request, "با موفقیت وارد شدید!")
                    return JsonResponse(
                        {
                            "status": "redirect",
                            "redirect_url": redirect_url,
                        }
                    )
                else:
                    messages.info(
                        request,
                        "حساب شما فعال نیست. لطفاً شماره تلفن خود را تأیید کنید.",
                    )
                    user.code.save()
                    request.session["user_id"] = user.id
                    return redirect(f"{reverse('verifyCode')}?next={redirect_url}")

            else:
                messages.error(
                    request,
                    "شماره تلفن یا رمز عبور اشتباه است.",
                )
        else:
            messages.error(request, "لطفاً شماره تلفن و رمز عبور را وارد کنید.")

    return JsonResponse(
        {
            "status": "redirect",
            "redirect_url": redirect_url,
        }
    )


def httpVerifyCode(request):
    redirect_url = request.GET.get("next", "/")

    if request.user.is_authenticated:
        return JsonResponse(
            {
                "status": "redirect",
                "redirect_url": redirect_url,
            }
        )

    userId = request.session.get("user_id")
    if not userId:
        messages.error(request, "لطفاً ابتدا ثبت‌نام کنید یا وارد شوید.")

    user = get_object_or_404(User, id=userId)
    if request.method == "POST":
        form = VerifyCodeForm(request.POST)
        if form.is_valid():
            code_entered = form.cleaned_data["code"]
            try:
                user_code = Code.objects.get(user=user)
            except Code.DoesNotExist:
                messages.error(request, "برای این کاربر کدی یافت نشد.")

            if (user_code.number == code_entered) and user_code.tryCount > 0:
                user.is_phone_verified = True
                user.save()
                login(request, user)
                messages.success(request, "با موفقیت وارد شدید!")
                return JsonResponse(
                    {
                        "status": "redirect",
                        "redirect_url": redirect_url,
                    }
                )

            elif user_code.tryCount < 1:
                user_code.tryCount = 3
                user_code.save()
                messages.error(
                    request,
                    "حداکثر تلاش ناموفق. لطفاً با کد جدید ارسال شده مجدداً امتحان کنید.",
                )
            else:
                user_code.save_decrement_try_count()
                messages.error(request, "کد نامعتبر است. لطفاً دوباره تلاش کنید.")
    else:
        form = VerifyCodeForm()

    return render(
        request,
        "partials/verifyCode.html",
        {"form": form, "user": user, "next": redirect_url},
    )


@login_required
def httpAddAddress(request):
    redirect_url = request.GET.get("next", "/")
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, "آدرس جدید با موفقیت اضافه شد!")
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
        return redirect(redirect_url)

    states = settings.IRAN_PROVINCES_CHOICES
    return render(
        request, "partials/address.html", {"states": states, "next": redirect_url}
    )


@login_required
def set_current_address(request):
    if request.method == "POST":
        data = json.loads(request.body)
        selected_address_id = data.get("selected_address")
        try:
            address = Address.objects.get(id=selected_address_id, user=request.user)
            Address.objects.filter(user=request.user, isCurrent=True).update(
                isCurrent=False
            )
            address.isCurrent = True
            address.save()
            return JsonResponse(
                {
                    "title": "موفقیت‌آمیز",
                    "message": "آدرس با موفقیت به‌روز شد!",
                    "icon": "success",
                }
            )
        except Address.DoesNotExist:
            return JsonResponse(
                {
                    "title": "خطا",
                    "message": "آدرس انتخاب‌شده معتبر نیست.",
                    "icon": "error",
                }
            )

    return JsonResponse(
        {"title": "خطا", "message": "درخواست نامعتبر.", "icon": "error"}
    )


@login_required
def delete_address(request):
    if request.method == "POST":
        data = json.loads(request.body)
        address_id = data.get("address_id")

        try:
            address = Address.objects.get(id=address_id, user=request.user)

            # Check if the address is the primary address
            if address.isCurrent:
                return JsonResponse(
                    {
                        "status": "error",
                        "title": "خطا",
                        "message": "نمی‌توانید آدرس اصلی خود را حذف کنید.",
                        "icon": "error",
                    }
                )

            # Delete the address if it's not the primary address
            address.delete()

            updated_html = render_to_string(
                "partials/address_list.html", {"user": request.user}
            )

            return JsonResponse(
                {
                    "status": "success",
                    "title": "موفقیت‌آمیز",
                    "message": "آدرس با موفقیت حذف شد!",
                    "icon": "success",
                    "updated_html": updated_html,
                }
            )
        except Address.DoesNotExist:
            return JsonResponse(
                {
                    "status": "error",
                    "title": "خطا",
                    "message": "آدرسی یافت نشد.",
                    "icon": "error",
                }
            )

    return JsonResponse(
        {
            "status": "error",
            "title": "خطا",
            "message": "درخواست نامعتبر.",
            "icon": "error",
        }
    )


def httpLoginByCode(request):
    redirect_url = request.GET.get("next", "/")
    if request.user.is_authenticated:
        return JsonResponse(
            {
                "status": "redirect",
                "redirect_url": redirect_url,
            }
        )

    if request.method == "POST":
        form = LoginByCodeForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            user = User.objects.filter(username=phone_number).first()
            if user:
                user.code.save()
                request.session["user_id"] = user.id
                return redirect(f"{reverse('verifyCode')}?next={redirect_url}")
            else:
                messages.error(request, "شماره تلفن نامعتبر است.")
        else:
            messages.error(request, "لطفاً شماره تلفن خود را وارد کنید.")

    return render(
        request,
        "partials/login_by_code.html",
        {"form": LoginByCodeForm(), "next": redirect_url},
    )


@login_required
def httpLogout(request):
    logout(request)
    messages.success(request, "با موفقیت خارج شدید!")
    redirect_url = request.GET.get("next", "/")
    return redirect(redirect_url)
