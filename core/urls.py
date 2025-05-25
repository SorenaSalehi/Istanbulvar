from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib import admin


urlpatterns = [
    path("", include("users.urls")),
    path("", include("website.urls")),
    path("admin/", admin.site.urls),
    path("shop/", include("shop.urls")),
    path("payment/", include("payment.urls")),
    path("summernote/", include("django_summernote.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
