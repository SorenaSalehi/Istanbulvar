from django.db import models
from django.contrib.auth.models import AbstractUser
from random import randrange
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import requests
import os

SMS_API_KEY = os.getenv("SMS_API_KEY")
SMS_API_ID = os.getenv("SMS_API_ID")


class CustomUser(AbstractUser):
    phone_number = models.CharField(
        max_length=10,
        verbose_name="شماره تلفن"
    )
    is_email_verified = models.BooleanField(
        default=False,
        verbose_name="تأیید ایمیل"
    )
    is_phone_verified = models.BooleanField(
        default=False,
        verbose_name="تأیید شماره تلفن"
    )


class Code(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    number = models.CharField(max_length=5, blank=True)
    tryCount = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.user.get_full_name()} — {self.number}"

    def save(self, *args, **kwargs):
        # تولید کد جدید و ارسال پیامک
        self.number = str(randrange(10000, 99999))
        sms(self.number, self.user.phone_number)
        super().save(*args, **kwargs)

    def save_decrement_try_count(self, *args, **kwargs):
        """
        کاهش یک واحد از tryCount بدون تولید کد جدید.
        """
        self.tryCount -= 1
        super(Code, self).save(update_fields=["tryCount"], *args, **kwargs)
    class Meta:
        verbose_name = "کد تایید"
        verbose_name_plural = "کد های تایید"



class Address(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="addresses",
    )
    first_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="نام"
    )
    last_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="نام خانوادگی"
    )
    street = models.CharField(
        max_length=255,
        verbose_name="آدرس"
    )
    city = models.CharField(
        max_length=100,
        verbose_name="شهر"
    )
    apartment = models.CharField(
        max_length=100,
        verbose_name="جزئیات آدرس",
        blank=True,
        null=True
    )
    country = models.CharField(
        max_length=100,
        choices=settings.COUNTRY_CHOICES,
        default="Iran",
        verbose_name="کشور"
    )
    state = models.CharField(
        max_length=100,
        verbose_name="استان",
        default="تهران"
    )

    isCurrent = models.BooleanField(default=True)
    is_corporate = models.BooleanField(
        default=False,
        verbose_name="آیا شرکتی است؟"
    )
    tax_office = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="اداره مالیاتی"
    )
    company_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="نام شرکت"
    )
    tax_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="شناسه مالیاتی"
    )

    def __str__(self):
        return f"{self.street}, {self.city}"

    def clean(self):
        """
        اگر آدرس شرکتی است، فیلدهای اداره مالیاتی، نام شرکت و شناسه مالیاتی اجباری باشند.
        """
        if self.is_corporate:
            if not self.tax_office:
                raise ValidationError({
                    "tax_office": "وارد کردن اداره مالیاتی الزامی است."
                })
            if not self.company_name:
                raise ValidationError({
                    "company_name": "وارد کردن نام شرکت الزامی است."
                })
            if not self.tax_id:
                raise ValidationError({
                    "tax_id": "وارد کردن شناسه مالیاتی الزامی است."
                })

    def save(self, *args, **kwargs):
        if self.isCurrent:
            Address.objects.filter(user=self.user).update(isCurrent=False)
        self.full_clean()
        super().save(*args, **kwargs)

    def getAddress(self):
        return f"{self.street}{', ' + self.apartment if self.apartment else ''}, {self.city}/{self.state}"
    
    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"


@receiver(post_save, sender=CustomUser)
def codeGenerator(sender, instance, created, **kwargs):
    if created:
        code = Code(user=instance)
        code.save()


def sms(code, number):
    print(number," ",code)
