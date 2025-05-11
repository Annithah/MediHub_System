from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('auth_application.urls', namespace='auth_application')),
    path('appointment/', include('appointment_app.urls', namespace='appointment_app')),
    path('i18n/', include('django.conf.urls.i18n')),
    #path('patient/', include('patient_management_app.urls', namespace='patient_management_app')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)