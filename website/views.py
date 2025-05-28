from django.shortcuts import redirect, render
from shop.models import Product, Order, SpecialOffer, Brand
from .forms import CustomerContactForm, RetailerContactForm
from .models import Banner, Newsletter
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


def httpIndex(request):
    headerBanners = Banner.objects.filter(section="home_header")
    NewProductsBanner = Banner.objects.filter(section="new_products")

    top_products = Product.objects.order_by("-rating")[:10]
    new_products = Product.objects.order_by("-created_at")[:8]
    group1 = new_products[:4]
    group2 = new_products[4:8]

    now = timezone.now()

    offers = None
    nearestEnd = None
    if request.user.is_authenticated:

        user_group_ids = request.user.groups.values_list("id", flat=True)

        offers = (
            SpecialOffer.objects.filter(start_date__lte=now, end_date__gte=now)
            .filter(
                Q(users__isnull=True, groups__isnull=True)
                | Q(users=request.user)
                | Q(groups__in=user_group_ids)
            )
            .distinct()
            .order_by("-end_date")
        )

        if offers:
            active_offers = SpecialOffer.objects.filter(
                start_date__lte=now, end_date__gte=now
            ).values_list("end_date", flat=True)
            nearestEnd = min(active_offers)

    return render(
        request,
        "index.html",
        {
            "NewProductsBanner": NewProductsBanner,
            "headerBanners": headerBanners,
            "topProducts": top_products,
            "newProducts1": group1,
            "newProducts2": group2,
            "specialOffers": offers,
            "nearestEnd": nearestEnd,
        },
    )


def httpOrders(request):

    if not request.user.is_authenticated:
        return redirect("website:index")

    current_status = request.GET.get("status", "")

    sort = request.GET.get("sort", "date")
    direction = request.GET.get("dir", "desc")
    if sort == "total":
        order_field = "total_price"
    else:
        order_field = "created_at"
    if direction == "desc":
        order_field = f"-{order_field}"

    qs = Order.objects.filter(user=request.user)
    if current_status:
        qs = qs.filter(status=current_status)
    qs = qs.order_by(order_field)

    paginator = Paginator(qs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "account/orders.html",
        {
            "orders": page_obj,
            "page_obj": page_obj,
            "current_sort": sort,
            "current_dir": direction,
            "current_status": current_status,
        },
    )


def httpAbout(request):
    brands = Brand.objects.all()

    return render(request, "about.html", {"brands": brands})


def httpMSS(request):
    return render(request, "mss.html")


def httpGP(request):
    return render(request, "gp.html")


def httpOrderAndRefound(request):
    return render(request, "order-refound.html")


def httpContact(request):
    return render(request, "contact.html")


@csrf_exempt
def addNewsletter(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")

            if not email:
                return JsonResponse(
                    {"success": False, "message": "ایمیل وارد نشده است."}
                )

            if Newsletter.objects.filter(email=email).exists():
                return JsonResponse(
                    {"success": False, "message": "این ایمیل قبلاً ثبت شده است."}
                )

            Newsletter.objects.create(email=email)
            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"success": False, "message": "خطا در پردازش اطلاعات."})

    return JsonResponse({"success": False, "message": "درخواست نامعتبر است."})


def customer_contact_view(request):
    if request.method == "POST":
        form = CustomerContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Mesajınız bize ulaştı, en kısa sürede sizinle iletişimie geçeceğiz",
            )
        else:
            messages.error(
                request,
                "Mesajınızı yoğunluktan dolayı alamadık, bize direkt telefon numaradan ulaşabilirsiniz  !",
            )
    return render(request, "contact.html")


def retailer_contact_view(request):
    if request.method == "POST":
        form = RetailerContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Mesajınız bize ulaştı, en kısa sürede sizinle iletişimie geçeceğiz",
            )
        else:
            messages.error(
                request,
                "Mesajınızı yoğunluktan dolayı alamadık, bize direkt telefon numaradan ulaşabilirsiniz  !",
            )
    return render(request, "contact.html")
