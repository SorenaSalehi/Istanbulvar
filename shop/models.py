from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.contrib.auth import user_logged_in
from django.dispatch import receiver
from django.db import models
from users.models import Address
from PIL import Image
from io import BytesIO
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import os

User = get_user_model()


class Category(models.Model):
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="دسته‌بندی والد",
    )
    name = models.CharField(
        max_length=100,
        unique=False,
        verbose_name="نام دسته‌بندی",
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        verbose_name="شناسه یکتا",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        names = [self.name]
        parent = self.parent
        while parent:
            names.append(parent.name)
            parent = parent.parent
        return " > ".join(reversed(names))

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"


class Brand(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="نام برند",
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        verbose_name="شناسه یکتا",
    )
    description = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="توضیحات",
    )
    img = models.ImageField(
        upload_to="brands/banner",
        default="brands/defaults/default_banner.webp",
        blank=True,
        verbose_name="تصویر بنر برند",
    )
    logo = models.ImageField(
        upload_to="brands/logo",
        default="brands/defaults/default_logo.webp",
        blank=True,
        verbose_name="لوگو برند",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برندها"


class Attribute(models.Model):
    TYPE = [
        ("attributes", "ویژگی‌ها"),
        ("variants", "محصولات مرتبط"),
    ]
    name = models.CharField(
        max_length=100,
        verbose_name="نام ویژگی",
    )
    attribute_type = models.CharField(
        max_length=10,
        choices=TYPE,
        default="attributes",
        verbose_name="نوع ویژگی",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ویژگی"
        verbose_name_plural = "ویژگی‌ها"


class AttributeValue(models.Model):
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        verbose_name="ویژگی",
    )
    key = models.CharField(
        max_length=100,
        verbose_name="کلید ویژگی",
    )
    value = models.CharField(
        max_length=100,
        verbose_name="مقدار ویژگی",
    )
    desc = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="توضیحات ویژگی",
    )

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"

    class Meta:
        verbose_name = "مقدار ویژگی"
        verbose_name_plural = "مقادیر ویژگی"


class ProductDetail(models.Model):
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        related_name="details",
        verbose_name="محصول",
    )
    title = models.CharField(
        max_length=100,
        verbose_name="عنوان",
    )
    description = models.TextField(
        verbose_name="توضیحات",
    )

    def __str__(self):
        return f"{self.product} - {self.title}"

    class Meta:
        verbose_name = "جزئیات محصول"
        verbose_name_plural = "جزئیات محصول"


class ProductDetailMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ("image", "تصویر"),
        ("video", "ویدئو"),
    ]
    MEDIA_POSITION_CHOICES = [
        ("center", "وسط"),
        ("left", "چپ"),
        ("right", "راست"),
    ]

    name = models.CharField(
        max_length=50,
        verbose_name="نام",
    )
    productDetail = models.ForeignKey(
        ProductDetail,
        on_delete=models.CASCADE,
        related_name="media",
        verbose_name="جزئیات محصول",
    )
    media_type = models.CharField(
        max_length=5,
        choices=MEDIA_TYPE_CHOICES,
        default="image",
        verbose_name="نوع رسانه",
    )
    media_position = models.CharField(
        max_length=10,
        choices=MEDIA_POSITION_CHOICES,
        default="center",
        verbose_name="موقعیت رسانه",
    )
    file = models.FileField(
        upload_to="product_detail_media/",
        blank=True,
        null=True,
        verbose_name="فایل رسانه",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
    )

    def __str__(self):
        return f"{self.productDetail.product} - {self.productDetail.title} - {self.media_type}"

    class Meta:
        verbose_name = "رسانه جزئیات محصول"
        verbose_name_plural = "رسانه جزئیات محصول"


class Product(models.Model):
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="محصول والد",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="کاربر",
    )
    name = models.CharField(
        max_length=200,
        verbose_name="نام محصول",
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        null=True,
        verbose_name="شناسه یکتا",
    )
    brand = models.ForeignKey(
        "Brand",
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="برند",
        blank=True,
        null=True,
    )
    category = models.ManyToManyField(
        "Category",
        related_name="products",
        verbose_name="دسته‌بندی",
        blank=True,
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="قیمت تخفیف‌خورده",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="قیمت",
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="موجودی",
    )
    sku = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
        verbose_name="شناسه انبار (SKU)",
    )
    attributes = models.ManyToManyField(
        "AttributeValue",
        blank=True,
        verbose_name="ویژگی‌ها",
    )
    rating = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="امتیاز (۰–۵)",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"


class RelatedProduct(models.Model):
    RELATED_TYPE_CHOICES = [
        ("similarity", "مشابه"),
        ("buy-together", "خرید با هم"),
    ]
    from_product = models.ForeignKey(
        Product,
        related_name="related_from",
        on_delete=models.CASCADE,
        verbose_name="محصول مبدا",
    )
    to_product = models.ForeignKey(
        Product,
        related_name="related_to",
        on_delete=models.CASCADE,
        verbose_name="محصول مقصد",
    )
    related_type = models.CharField(
        max_length=20,
        choices=RELATED_TYPE_CHOICES,
        default="similarity",
        verbose_name="نوع مرتبط‌سازی",
    )

    def __str__(self):
        return f"از {self.from_product} → به {self.to_product}"

    class Meta:
        verbose_name = "محصول مرتبط"
        verbose_name_plural = "محصولات مرتبط"


class Comment(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="محصول",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="کاربر",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        verbose_name="پاسخ به",
    )
    content = models.TextField(
        verbose_name="محتوا",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی",
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name="فعال",
    )
    rating = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="امتیاز (۰–۵)",
    )

    def __str__(self):
        if self.user:
            return f"نظر #{self.id} توسط {self.user.username}"
        return f"نظر #{self.id}"

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"


class CommentMedia(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="media",
        verbose_name="نظر",
    )
    image = models.ImageField(
        upload_to="comment_media/",
        verbose_name="تصویر",
    )
    thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFill(205, 205)],
        format="WEBP",
        options={"quality": 60},
    )

    def __str__(self):
        return str(self.comment)

    class Meta:
        verbose_name = "رسانه نظر"
        verbose_name_plural = "رسانه‌های نظر"


class ProductMedia(models.Model):
    MEDIA_TYPE_CHOICES = [
        ("image", "تصویر"),
        ("video", "ویدئو"),
    ]

    name = models.CharField(
        max_length=50,
        verbose_name="نام",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="media",
        verbose_name="محصول",
    )
    media_type = models.CharField(
        max_length=5,
        choices=MEDIA_TYPE_CHOICES,
        default="image",
        verbose_name="نوع رسانه",
    )
    file = models.FileField(
        upload_to="product_media/",
        verbose_name="فایل رسانه",
    )
    thumbnail = models.ImageField(
        upload_to="product_media/",
        blank=True,
        null=True,
        verbose_name="تصویر بندانگشتی",
    )
    normal_size = models.ImageField(
        upload_to="product_media/",
        blank=True,
        null=True,
        verbose_name="سایز معمول",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
    )

    def __str__(self):
        return f"{self.product.name} - {self.media_type}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.media_type == "image" and self.file:
            original_path = self.file.path
            if not os.path.exists(original_path):
                return
            base_name = os.path.splitext(os.path.basename(self.file.name))[0]

            with Image.open(original_path) as main_img:
                main_img = main_img.resize((665, 665), Image.LANCZOS)
                buf = BytesIO()
                main_img.save(buf, format="WEBP", quality=90)
                self.file.save(f"{base_name}.webp", ContentFile(buf.getvalue()), save=False)

            with Image.open(self.file.path) as thumb_img:
                thumb_img = thumb_img.resize((205, 205), Image.LANCZOS)
                buf = BytesIO()
                thumb_img.save(buf, format="WEBP", quality=90)
                self.thumbnail.save(f"{base_name}-thumb.webp", ContentFile(buf.getvalue()), save=False)

            with Image.open(self.file.path) as normal_img:
                normal_img = normal_img.resize((435, 435), Image.LANCZOS)
                buf = BytesIO()
                normal_img.save(buf, format="WEBP", quality=90)
                self.normal_size.save(f"{base_name}-normal.webp", ContentFile(buf.getvalue()), save=False)

            try:
                os.remove(original_path)
            except OSError:
                pass

            super().save(update_fields=["file", "thumbnail", "normal_size"])
        elif self.media_type == "video" and self.normal_size:
            original_path = self.normal_size.path
            if not os.path.exists(original_path):
                return
            base_name = os.path.splitext(os.path.basename(self.normal_size.name))[0]

            with Image.open(original_path) as normal_img:
                normal_img = normal_img.resize((435, 435), Image.LANCZOS)
                buf = BytesIO()
                normal_img.save(buf, format="WEBP", quality=90)
                self.normal_size.save(f"{base_name}-normal.webp", ContentFile(buf.getvalue()), save=False)

            with Image.open(original_path) as thumb_img:
                thumb_img = thumb_img.resize((205, 205), Image.LANCZOS)
                buf = BytesIO()
                thumb_img.save(buf, format="WEBP", quality=90)
                self.thumbnail.save(f"{base_name}-thumb.webp", ContentFile(buf.getvalue()), save=False)

            try:
                os.remove(original_path)
            except OSError:
                pass

            super().save(update_fields=["file", "thumbnail", "normal_size"])
        else:
            raise ValueError("برای ویدئو باید تصویر normal_size وجود داشته باشد.")

    class Meta:
        verbose_name = "رسانه محصول"
        verbose_name_plural = "رسانه‌های محصول"


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="carts",
        verbose_name="کاربر",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی",
    )

    def __str__(self):
        if self.user:
            return f"سبد خرید کاربر {self.user.username} - #{self.id}"
        return f"سبد خرید مهمان - #{self.id}"

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبدهای خرید"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="سبد خرید",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="محصول",
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="تعداد",
    )

    def __str__(self):
        return f"{self.quantity}x {self.product}"

    class Meta:
        verbose_name = "آیتم سبد خرید"
        verbose_name_plural = "آیتم‌های سبد خرید"


class ShippingCarrier(models.Model):
    name = models.CharField(
        "نام پیک",
        max_length=100,
        unique=True,
    )
    slug = models.SlugField(
        "شناسه یکتا",
        max_length=100,
        unique=True,
    )
    logo = models.ImageField(
        "لوگو",
        upload_to="shipping_carriers/",
        blank=True,
        null=True,
        help_text="اختیاری: لوگوی پیک برای نمایش در فرانت‌اند",
    )
    tracking_url = models.CharField(
        "قالب لینک رهگیری",
        max_length=255,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "پیک ارسال"
        verbose_name_plural = "پیک‌های ارسال"

    def get_tracking_link(self, tracking_number: str) -> str:
        return self.tracking_url.format(tracking_number=tracking_number)


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "سفارش ثبت شد"),
        ("paid", "پرداخت انجام شد"),
        ("payment_failed", "پرداخت ناموفق"),
        ("preparing", "در حال آماده‌سازی"),
        ("shipped", "ارسال شد"),
        ("delivered", "تحویل داده شد"),
        ("canceled", "لغو شد"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="کاربر",
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="آدرس",
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="شماره تلفن",
    )
    email = models.EmailField(
        verbose_name="ایمیل",
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="وضعیت سفارش",
    )
    shipping_carrier = models.ForeignKey(
        ShippingCarrier,
        on_delete=models.PROTECT,
        verbose_name="پیک انتخاب‌شده",
        null=True,
        blank=True,
    )
    tracking_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="شماره رهگیری",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی",
    )
    estimated_delivery = models.DateField(
        blank=True,
        null=True,
        verbose_name="تاریخ تحویل تخمینی",
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="مبلغ کل",
    )

    def __str__(self):
        return f"سفارش #{self.id}"

    @property
    def status_color(self):
        colors = {
            "pending": "secondary",
            "paid": "success",
            "payment_failed": "danger",
            "preparing": "warning",
            "shipped": "info",
            "delivered": "success",
            "canceled": "dark",
        }
        return colors.get(self.status, "light")

    @property
    def tracking_url(self):
        if self.shipping_carrier and self.tracking_number:
            return self.shipping_carrier.get_tracking_link(self.tracking_number)
        return ""

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name="سفارش",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="محصول",
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="تعداد",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="قیمت واحد",
    )

    def __str__(self):
        return f"{self.quantity}x {self.product}"

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"


class Wishlist(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="wishlist",
        null=True,
        blank=True,
        verbose_name="کاربر",
    )
    products = models.ManyToManyField(
        Product,
        blank=True,
        related_name="wishlisted_by",
        verbose_name="محصولات موردعلاقه",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ به‌روزرسانی",
    )

    def __str__(self):
        if self.user:
            return f"لیست علاقه‌مندی‌های {self.user.username}"
        return f"لیست علاقه‌مندی‌های مهمان - #{self.id}"

    class Meta:
        verbose_name = "لیست علاقه‌مندی"
        verbose_name_plural = "لیست‌های علاقه‌مندی"



class SpecialOffer(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, related_name="offers")
    users = models.ManyToManyField(User, blank=True, related_name="personal_offers")
    groups = models.ManyToManyField(
        "auth.Group", blank=True, related_name="group_offers"
    )
    discount_percent = models.PositiveSmallIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=["start_date", "end_date"]),
        ]

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def __str__(self):
        return f"{self.name} ({self.discount_percent}%)"


@receiver(user_logged_in)
def merge_cart_on_login(sender, user, request, **kwargs):
    cart_id = request.session.get("cart_id")
    if not cart_id:
        return

    try:
        guest_cart = Cart.objects.get(pk=cart_id, user__isnull=True)
    except Cart.DoesNotExist:
        return

    user_cart, created = Cart.objects.get_or_create(user=user)
    for item in guest_cart.items.all():
        user_cart_item, new_item_created = CartItem.objects.get_or_create(
            cart=user_cart, product=item.product
        )
        user_cart_item.quantity += item.quantity
        user_cart_item.save()

    guest_cart.delete()
    del request.session["cart_id"]


@receiver(user_logged_in)
def merge_wishlist_on_login(sender, user, request, **kwargs):
    wishlist_id = request.session.get("wishlist_id")
    if not wishlist_id:
        return

    try:
        guest_wishlist = Wishlist.objects.get(pk=wishlist_id, user__isnull=True)
    except Wishlist.DoesNotExist:
        return

    user_wishlist, created = Wishlist.objects.get_or_create(user=user)
    user_wishlist.products.add(*guest_wishlist.products.all())

    guest_wishlist.delete()
    del request.session["wishlist_id"]
