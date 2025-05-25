from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaulttags import register
from .models import (
    Brand,
    Order,
    OrderItem,
    Product,
    CartItem,
    Cart,
    Category,
    Wishlist,
    AttributeValue,
)
from users.models import Address
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.contrib import messages
import json
from payment.views import payment_iframe
from django.db.models import Q

FREE_SHIPPING_THRESHOLD = 5000

def shop_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()

    # --- APPLY FILTERS ---

    # محصولات تخفیف خورده
    discount = request.GET.get("discount")
    if discount:
        products = products.filter(discount_price__isnull=False)

    # فیلتر دسته‌بندی (checkbox با name="category")
    selected_cats = request.GET.getlist("category")
    if selected_cats:
        products = products.filter(category__in=selected_cats)

    # فیلتر برند (checkbox با name="brand")
    selected_brands = request.GET.getlist("brand")
    if selected_brands:
        products = products.filter(brand__in=selected_brands)

    # فیلتر محدوده قیمت (inputs با name="min_price" / "max_price")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # فیلتر ویژگی‌های داینامیک (checkbox با name="attr_<key>")
    attribute_keys = AttributeValue.objects.values_list("key", flat=True).distinct()
    for key in attribute_keys:
        values = request.GET.getlist(f"attr_{key}")
        if values:
            products = products.filter(
                attributes__key=key, attributes__value__in=values
            )

    products = products.distinct()
    prodCount = products.count()

    # --- PAGINATE ---
    paginator = Paginator(products, 9)  # 9 آیتم در هر صفحه
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # --- بازسازی تعداد برای سایدبار (بدون تغییر) ---
    attributes = AttributeValue.objects.all()
    attributesDict = {}
    for attr in attributes:
        count = Product.objects.filter(
            attributes__attribute__name=attr.attribute.name,
            attributes__key=attr.key,
            attributes__value=attr.value,
        ).count()
        if count:
            if attr.attribute.attribute_type == "attributes":
                attributesDict.setdefault(attr.attribute.name, []).append(
                    {
                        "id": attr.id,
                        "name": f"{attr.key}  :  {attr.value}",
                        "count": count,
                    }
                )
            else:
                attributesDict.setdefault(attr.attribute.name, []).append(
                    {"id": attr.id, "name": attr.value, "count": count}
                )

    get_params = request.GET.copy()
    if "page" in get_params:
        get_params.pop("page")
    return render(
        request,
        "shop.html",
        {
            "categories": categories,
            "proudCount":prodCount,
            "brands": brands,
            "attributesDict": attributesDict,
            "page_obj": page_obj,
            "paginator": paginator,
            "get_params": get_params,
        },
    )



def product_view(request, product_slug):

    product = get_object_or_404(Product, slug=product_slug)
    root = product.parent or product
    all_variants = Product.objects.filter(Q(parent=root) | Q(id=root.id)).distinct()
    similar_products = Product.objects.filter(
        Q(related_to__from_product=product, related_to__related_type="similarity")
        | Q(related_from__to_product=product, related_from__related_type="similarity")
    ).distinct()
    context = {
        "root": root,
        "all_variants": all_variants,
        "rating_breakdown": ratingBreakdown(product),
        "similar_products": similar_products,
        "all_details": root.details.all(),
    }

    route = request.resolver_match.url_name
    isExist = True
    current_filters = {}

    if request.method == "POST":
        post_data = request.POST.copy()
        post_data.pop("csrfmiddlewaretoken", None)

        allProducts = Product.objects.filter(Q(parent=root) | Q(id=root.id)).distinct()

        for key, value in post_data.items():
            allProducts = allProducts.filter(
                attributes__key=key,
                attributes__value=value
            )
        products = allProducts.distinct()

        try:
            product = products[0]
        except IndexError:
            isExist = False

        current_filters = {k: v for k, v in post_data.items() if v}

    else:
        # حالت GET: فیلترهای پیش‌فرض از خود محصول
        for attr in product.attributes.filter(attribute__attribute_type="variants"):
            current_filters[attr.key] = attr.value

    # ساخت گزینه‌های فیلتر
    choices = {}
    for variant in all_variants:
        for x in variant.attributes.filter(attribute__attribute_type="variants"):
            choices.setdefault(x.key, set()).add(x.value)

    attribute_options = {}
    attribute_id = 1
    for name, values in choices.items():
        opts = []
        for value in sorted(values):
            selected = current_filters.get(name) == value
            opts.append({
                "value": value,
                "id": attribute_id,
                "selected": selected,
            })
            attribute_id += 1
        attribute_options[name] = opts

    # افزدون به کانتکست و رندر
    context.update({
        "attributes": attribute_options,
        "isExist": isExist,
    })
    template = "single-product/product-detail.html"
    context["product"]=product

    if route == "product_attribute":

        # همه واریانت‌ها به‌جز خود محصول
        variants = Product.objects.filter(
            parent=root
        ).exclude(slug=product.slug)
        variants = list(variants)
        # اگر خود محصول واریانت بود، والدشو هم اضافه کن
        if product.parent:
            variants.append(product.parent)

        # جمع‌آوری همه attributes
        attributes = {}
        for variant in variants + [product]:
            for x in variant.attributes.all():
                attributes.setdefault(x.attribute.name, set()).add(x.value)

        context.update({
            "variants": variants,
            "attributes": attributes,
        })
        template = "single-product/product-attribute.html"


    elif route == "product_review":
        # --- کامنت‌ها و صفحه‌بندی ---
        comments_list = product.comments.all().order_by("-created_at")
        paginator = Paginator(comments_list, 10)
        page_number = request.GET.get("page")
        comments_page = paginator.get_page(page_number)

        context.update({
            "comments_page": comments_page,
        })
        template = "single-product/product-review.html"


    return render(request, template, context)

def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    root = product.parent or product
    all_variants = Product.objects.filter(Q(parent=root) | Q(id=root.id)).distinct()


    current_filters = {}
    isExist = True
    if request.method == "POST":
        post_data = request.POST.copy()
        post_data.pop("csrfmiddlewaretoken", None)
        root = product.parent or product
        
        allProducts = Product.objects.filter(Q(parent=root) | Q(id=root.id)).distinct()

        for key, value in post_data.items():
            allProducts = allProducts.filter(
                attributes__key=key, attributes__value=value
            )
        products = allProducts.distinct()


        try:
            product = products[0]
        except:
            isExist = False

        current_filters = {k: v for k, v in post_data.items() if v}
    else:
        for attr in product.attributes.filter(attribute__attribute_type="variants"):
            current_filters[attr.key] = attr.value

    choices = {}
    for variant in all_variants:
        for x in variant.attributes.filter(attribute__attribute_type="variants"):
            choices.setdefault(x.key, set()).add(x.value)

    attribute_options = {}
    attributeId = 1
    for name, values in choices.items():
        opts = []
        for value in sorted(values):
            selected = current_filters.get(name) == value
            test_filters = current_filters.copy()
            test_filters[name] = value

            opts.append(
                {
                    "value": value,
                    "id":attributeId,
                    "selected": selected,
                }
            )
            attributeId += 1
        attribute_options[name] = opts
    

    similar_products = Product.objects.filter(
        Q(related_to__from_product=product, related_to__related_type="similarity")
        | Q(related_from__to_product=product, related_from__related_type="similarity")
    ).distinct()

    context = {
        "product": product,
        "attributes": attribute_options,
        "rating_breakdown": ratingBreakdown(product),
        "similar_products": similar_products,
        "allDetails":root.details.all(),
        "isExist": isExist,
    }

    

    return render(request, "single-product/product-detail.html", context)

def product_attributes(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    variants = Product.objects.filter(
        parent=product.parent if product.parent else product
    ).exclude(slug=product.slug)

    variants = list(variants)
    if product.parent:
        variants = variants + [product.parent]

    attributes = {}
    for variant in variants + [product]:
        for x in variant.attributes.all():
            if x.attribute.name not in attributes:
                attributes[x.attribute.name] = set()
            attributes[x.attribute.name].add(x.value)

    similar_products = Product.objects.filter(
        Q(related_to__from_product=product, related_to__related_type="similarity")
        | Q(related_from__to_product=product, related_from__related_type="similarity")
    ).distinct()

    context = {
        "product": product,
        "variants": variants,
        "attributes": attributes,
        "rating_breakdown": ratingBreakdown(product),
        "similar_products": similar_products,
    }

    return render(request, "single-product/product-attribute.html", context)

def product_review(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    similar_products = Product.objects.filter(
        Q(related_to__from_product=product, related_to__related_type="similarity")
        | Q(related_from__to_product=product, related_from__related_type="similarity")
    ).distinct()

    comments_list = product.comments.all().order_by("-created_at")
    paginator = Paginator(comments_list, 10)
    page_number = request.GET.get("page")
    comments_page = paginator.get_page(page_number)

    context = {
        "product": product,
        "rating_breakdown": ratingBreakdown(product),
        "similar_products": similar_products,
        "comments_page": comments_page,
    }

    return render(request, "single-product/product-review.html", context)

def ratingBreakdown(product):
    comments = product.comments.filter(is_active=True)
    total_comments = comments.count()

    stars_count = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    for comment in comments:
        stars = int(round(comment.rating))
        stars_count[stars] += 1

    rating_breakdown = []
    for star in [5, 4, 3, 2, 1]:
        count = stars_count[star]
        percentage = (count * 100 / total_comments) if total_comments else 0
        rating_breakdown.append(
            {
                "star": star,
                "count": count,
                "percentage": round(percentage, 1),
            }
        )
    return rating_breakdown

def cart_partial(request):
    cart = get_or_create_cart(request)
    try:
        items = cart.items.all()
        total_price = sum(
            (item.product.discount_price or item.product.price) * item.quantity
            for item in items
        )
        return render(
            request,
            "partials/cart_items.html",
            {"cart_items": items, "total_price": total_price},
        )
    except Cart.DoesNotExist:
        return render(
            request, "partials/cart_items.html", {"cart_items": [], "total_price": 0}
        )

def wishlist_partial(request):
    wishlist = get_or_create_wishlist(request)
    items = wishlist.products.all()
    wishlist_count = items.count()
    return render(
        request,
        "partials/wishlist_items.html",
        {"wishlist_items": items, "wishlist_count": wishlist_count},
    )

def checkOut(request):
    if request.method == "POST":
        if cop := checkOutPost(request):
            return cop

    context = {
        "cart_items": [],
        "total_price": 0,
        "cargo": 0,
        "total_ordered_price": 0,
        "states": settings.IRAN_PROVINCES_CHOICES,
    }

    cart = get_or_create_cart(request)
    try:
        items = cart.items.all()
        total_price = sum(
            (item.product.discount_price or item.product.price) * item.quantity
            for item in items
        )
        context.update(
            {
                "cart_items": items,
                "total_price": total_price,
                "cargo": 100 if 0 < total_price < FREE_SHIPPING_THRESHOLD else 0,
                "total_ordered_price": total_price + (100 if 0 < total_price < FREE_SHIPPING_THRESHOLD else 0),
            }
        )
        return render(request, "checkout/checkout.html", context)
    except Cart.DoesNotExist:
        return render(request, "checkout/checkout.html", context)

def checkOutPost(request):
    selected_address = request.POST.get("selected_address")
    state = request.POST.get("state")
    street = request.POST.get("street")
    apartment = request.POST.get("apartment")
    city = request.POST.get("city")
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    phone = request.POST.get("phone")
    email = request.POST.get("email")
    company_name = request.POST.get("company_name")
    tax_office = request.POST.get("tax_office")
    tax_id = request.POST.get("tax_id")
    is_corporate = request.POST.get("is_corporate")

    cart = get_or_create_cart(request)

    if cart.items.count() == 0:
        messages.error(request, "سبد خرید شما خالی است. لطفاً ابتدا محصولی به سبد اضافه کنید.")
        return

    # بررسی موجودی انبار
    for cart_item in cart.items.all():
        if cart_item.quantity > cart_item.product.stock:
            cart_item.quantity = cart_item.product.stock
            cart_item.save()
            messages.error(
                request,
                f"از محصول {cart_item.product.name} به اندازه کافی در انبار موجود نیست. حداکثر تعداد سفارش {cart_item.product.stock} عدد می‌تواند باشد.",
            )
            return

    if request.user.is_authenticated:
        order = Order(user=request.user)
        order.phone = request.user.phone_number
        order.email = request.user.email
    else:
        order = Order()

    # ذخیره آدرس و اطلاعات سفارش
    if state and street and city and phone and email and first_name and last_name:
        newAddress = Address(
            state=state,
            street=street,
            apartment=apartment,
            city=city,
            first_name=first_name,
            last_name=last_name,
        )
        if is_corporate:
            newAddress.company_name = company_name
            newAddress.tax_office = tax_office
            newAddress.tax_id = tax_id
        if request.user.is_authenticated:
            newAddress.user = request.user
        newAddress.save()

        order.address = newAddress
        order.phone = phone
        order.email = email

    elif selected_address:
        try:
            address = Address.objects.get(pk=selected_address)
            order.address = address
        except Address.DoesNotExist:
            messages.error(request, "آدرس انتخاب‌شده معتبر نیست.")
            return
    else:
        messages.error(request, "لطفاً اطلاعات آدرس خود را به طور کامل وارد کنید.")
        return

    order.save()

    # افزودن آیتم‌های سبد به سفارش
    if cart.items.count() > 0:
        for cart_item in cart.items.all():
            orderItem = OrderItem(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=(cart_item.product.discount_price or cart_item.product.price) * cart_item.quantity,
            )
            orderItem.save()
            order.total_price += orderItem.price

    # هزینه ارسال
    order.total_price += 100 if 0 < order.total_price < FREE_SHIPPING_THRESHOLD else 0
    order.save()

    return payment_iframe(request, order)

@login_required
def order_detail(request):
    data = json.loads(request.body)
    order_id = data.get("order_id")
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(
        request,
        "account/order_detail.html",
        {"order": order},
    )

@require_POST
def add_to_cart_api(request):
    cart = get_or_create_cart(request)
    data = json.loads(request.body)
    product_id = data.get("product_id")
    count = int(data.get("count", 1))
    title = ""
    icon = "success"

    if not product_id:
        return JsonResponse({
            "title": "خطا",
            "message": "محصول پیدا نشد.",
            "icon": "error",
            "cart_count": cart.items.count(),
        })

    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += count
        cart_item.save()
        msg = "سبد خرید به‌روزرسانی شد."
    else:
        cart_item.quantity = count
        cart_item.save()
        msg = "محصول به سبد اضافه شد."

    if cart_item.quantity > product.stock:
        if product.stock == 0:
            cart_item.delete()
            msg = "این محصول در انبار موجود نیست."
            icon = "error"
        else:
            msg = (
                f"شما می‌توانید حداکثر {product.stock} عدد از این محصول سفارش دهید.\n"
                f"تعداد موجود در سبد به {product.stock} عدد به‌روزرسانی شد."
            )
            icon = "info"
            cart_item.quantity = product.stock
            cart_item.save()
            if created:
                icon = "error"
                cart_item.delete()

    return JsonResponse({
        "title": title,
        "message": msg,
        "icon": icon,
        "cart_count": cart.items.count(),
    })

@require_POST
def remove_from_cart_api(request):
    cart = get_or_create_cart(request)
    data = json.loads(request.body)
    product_id = data.get("product_id")
    count = int(data.get("count", 1))
    title = ""
    icon = "success"

    if not product_id:
        return JsonResponse({
            "title": "خطا",
            "message": "محصول پیدا نشد.",
            "icon": "error",
            "cart_count": cart.items.count(),
        })

    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if count < cart_item.quantity:
            cart_item.quantity -= count
            cart_item.save()
            msg = "سبد خرید به‌روزرسانی شد."
        else:
            cart_item.delete()
            msg = "محصول از سبد حذف شد."

        if cart_item.quantity > product.stock:
            if product.stock == 0:
                cart_item.delete()
                msg = "این محصول در انبار موجود نیست."
                icon = "error"
            else:
                msg = (
                    f"شما می‌توانید حداکثر {product.stock} عدد از این محصول سفارش دهید.\n"
                    f"تعداد موجود در سبد به {product.stock} عدد به‌روزرسانی شد."
                )
                icon = "info"
                title = "تعداد محصول به‌روزرسانی شد"
                cart_item.quantity = product.stock
                cart_item.save()

        return JsonResponse({
            "title": title,
            "message": msg,
            "icon": icon,
            "cart_count": cart.items.count(),
        })

    except CartItem.DoesNotExist:
        return JsonResponse({
            "title": "خطا",
            "message": "این محصول در سبد شما وجود ندارد.",
            "icon": "error",
            "cart_count": cart.items.count(),
        })

@require_POST
def add_to_wishlist_api(request):
    wishlist = get_or_create_wishlist(request)
    data = json.loads(request.body)
    product_id = data.get("product_id")

    if not product_id:
        return JsonResponse({
            "title": "خطا",
            "message": "محصول پیدا نشد.",
            "icon": "error",
            "wishlist_count": wishlist.products.count(),
        })

    product = get_object_or_404(Product, id=product_id)
    if product in wishlist.products.all():
        title = "قبلاً اضافه شده"
        message = "این محصول قبلاً در لیست علاقه‌مندی شما وجود دارد."
        icon = "info"
    else:
        wishlist.products.add(product)
        title = "موفق"
        message = "محصول به لیست علاقه‌مندی شما اضافه شد."
        icon = "success"

    return JsonResponse({
        "title": title,
        "message": message,
        "icon": icon,
        "wishlist_count": wishlist.products.count(),
    })

@require_POST
def remove_from_wishlist_api(request):
    wishlist = get_or_create_wishlist(request)
    data = json.loads(request.body)
    product_id = data.get("product_id")

    if not product_id:
        return JsonResponse({
            "title": "خطا",
            "message": "محصول پیدا نشد.",
            "icon": "error",
            "wishlist_count": wishlist.products.count(),
        })

    product = get_object_or_404(Product, id=product_id)
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        title = "موفق"
        message = "محصول از لیست علاقه‌مندی شما حذف شد."
        icon = "success"
    else:
        title = "اطلاعات"
        message = "این محصول در لیست علاقه‌مندی شما وجود ندارد."
        icon = "info"

    return JsonResponse({
        "title": title,
        "message": message,
        "icon": icon,
        "wishlist_count": wishlist.products.count(),
    })

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            try:
                return Cart.objects.get(pk=cart_id, user__isnull=True)
            except Cart.DoesNotExist:
                pass
        new_cart = Cart.objects.create()
        request.session["cart_id"] = new_cart.id
        return new_cart

def get_cart(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).first()
    else:
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            return Cart.objects.filter(pk=cart_id, user__isnull=True).first()
        return

def get_or_create_wishlist(request):
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        return wishlist
    else:
        wishlist_id = request.session.get("wishlist_id", None)
        if wishlist_id:
            try:
                return Wishlist.objects.get(pk=wishlist_id, user__isnull=True)
            except Wishlist.DoesNotExist:
                pass
        new_wishlist = Wishlist.objects.create()
        request.session["wishlist_id"] = new_wishlist.id
        return new_wishlist

def get_wishlist(request):
    if request.user.is_authenticated:
        try:
            return Wishlist.objects.get(user=request.user)
        except Wishlist.DoesNotExist:
            pass
    else:
        wishlist_id = request.session.get("wishlist_id", None)
        if wishlist_id:
            try:
                return Wishlist.objects.get(pk=wishlist_id, user__isnull=True)
            except Wishlist.DoesNotExist:
                pass
    return

@register.filter
def get_range(value):
    return range(int(value))

@register.filter
def to_price(value):
    """
    تبدیل عدد به رشته قیمت با جداکننده هزارگان و واحد تومان
    مثال: 20000.00 -> '20,000.00 تومان'
    """
    try:
        return "{:,.2f} تومان".format(float(value))
    except (ValueError, TypeError):
        if value:
            return str(value) + " تومان"
        else:
            return ""

@register.filter
def to_int(value):
    return int(value)

@register.filter
def to_float(value):
    return float(value)

@register.filter
def discount_percentage(original_price, new_price):
    """
    محاسبه درصد تخفیف
    """
    try:
        original_price = float(original_price)
        new_price = float(new_price)
        if original_price == 0:
            return 0
        discount = ((original_price - new_price) / original_price) * 100
        return int(discount)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def add_decimal(value, arg):
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        return ""

@register.filter
def free_shipping_percentage(total_price) -> int:
    if total_price < FREE_SHIPPING_THRESHOLD:
        return int(total_price * 100 / FREE_SHIPPING_THRESHOLD)
    return 100

@register.filter
def remaining_for_free_shipping(total_price) -> int:
    if total_price < FREE_SHIPPING_THRESHOLD:
        return FREE_SHIPPING_THRESHOLD - total_price
    return 0

@register.filter
def sort_by_attr(queryset):
    try:
        return sorted(queryset, key=lambda item: item.attribute.name)
    except Exception:
        return queryset
