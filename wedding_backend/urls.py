from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('services/',include('services.urls')),
    path('accounts/',include('accounts.urls')),
    path('weddingprofile/',include('weddingprofile.urls')),
    path('orders/',include('orders.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
