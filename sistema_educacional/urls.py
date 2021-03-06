from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from cadastros import views
from django.conf.urls.static import static

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', include('web.urls')),
  path('cadastros/', include('cadastros.urls')),
  path('api/', include('api.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)