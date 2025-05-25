from django.contrib import admin
from .models import CustomerContact, RetailerContact


@admin.register(CustomerContact)
class CustomerContactAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "subject", "created_at")
    search_fields = ("first_name", "last_name", "email", "subject")


@admin.register(RetailerContact)
class RetailerContactAdmin(admin.ModelAdmin):
    list_display = ("company", "contact_person", "email", "subject", "created_at")
    search_fields = ("company", "contact_person", "email", "subject")
