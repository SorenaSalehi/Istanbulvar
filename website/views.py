from django.shortcuts import redirect, render
from shop.models import Product, Order
from .forms import CustomerContactForm, RetailerContactForm
from django.contrib import messages
from django.core.paginator import Paginator


def httpIndex(request):
    new_products = list(Product.objects.order_by("-id")[:8])

    group1 = new_products[:4]
    group2 = new_products[4:8]

    return render(
        request,
        "index.html",
        {
            "newProducts1": group1,
            "newProducts2": group2,
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
    return render(request, "about.html")


def httpMSS(request):
    return render(request, "mss.html")


def httpGP(request):
    return render(request, "gp.html")


def httpOrderAndRefound(request):
    return render(request, "order-refound.html")


def httpContact(request):
    return render(request, "contact.html")


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
