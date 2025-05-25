
from django.db import models

class PaymentLog(models.Model):
    orderId = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="شماره سفارش",
    )
    log = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="جزئیات",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد",
    )

    def __str__(self):
        return self.orderId
    
    class Meta:
        verbose_name = "گزارش پرداخت"
        verbose_name_plural = "گزارشات پرداخت"