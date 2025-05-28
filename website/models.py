from django.db import models


class CustomerContact(models.Model):
    first_name = models.CharField("Adınız", max_length=50)
    last_name = models.CharField("Soyadınız", max_length=50)
    email = models.EmailField("E-posta")
    phone = models.CharField("Telefon Numarası", max_length=20, blank=True, null=True)
    subject = models.CharField("Konu", max_length=100)
    message = models.TextField("Mesaj")
    created_at = models.DateTimeField("Oluşturulma Tarihi", auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"


class RetailerContact(models.Model):
    company = models.CharField("Firma Adı", max_length=100)
    contact_person = models.CharField("Yetkili Kişi", max_length=100)
    email = models.EmailField("E-posta")
    phone = models.CharField("Telefon Numarası", max_length=20, blank=True, null=True)
    website = models.URLField("Web Sitesi", blank=True, null=True)
    subject = models.CharField("Konu", max_length=100)
    message = models.TextField("Mesaj")
    created_at = models.DateTimeField("Oluşturulma Tarihi", auto_now_add=True)

    def __str__(self):
        return f"{self.company} - {self.subject}"



class Newsletter(models.Model):
    email = models.EmailField("E-posta")
    isActive = models.BooleanField(default=True)
    created_at = models.DateTimeField("Oluşturulma Tarihi", auto_now_add=True)

    def __str__(self):
        return self.email


class Banner(models.Model):
    # Display section choices
    SECTION_CHOICES = [
        ("home_header", "Home Page Header"),
        ("new_products", "Best of new product"),
        ("shop_list", "Catalog page banners"),
    ]

    section = models.CharField(
        max_length=20,
        choices=SECTION_CHOICES,
        default="home_header",
        help_text="Where this banner should appear on the site",
    )
    image = models.ImageField(
        upload_to="banners/%Y/%m/%d/", help_text="Banner image file"
    )
    title = models.CharField(
        max_length=100, blank=True, help_text="Optional title for the banner"
    )
    description = models.TextField(
        max_length=500, blank=True, help_text="Optional desc for the banner"
    )
    button_text = models.CharField(
        max_length=25, blank=True, help_text="name for the button"
    )
    link = models.URLField(
        max_length=300, blank=True, help_text="Optional URL to navigate to when clicked"
    )
    alt_text = models.CharField(
        max_length=150, blank=True, help_text="Alternative text for accessibility"
    )
    is_active = models.BooleanField(
        default=True, help_text="Toggle banner visibility without deleting it"
    )
    display_order = models.PositiveIntegerField(
        default=0, help_text="Lower numbers display first"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "-created_at"]
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

    def __str__(self):
        return f"{self.section} – {self.title or 'No Title'}"
