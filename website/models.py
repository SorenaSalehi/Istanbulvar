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
