from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('auth_application.urls', namespace='auth_application')),
    path('appointment/', include('appointment_app.urls', namespace='appointment_app')),
    path('patient/', include('patient_management_app.urls', namespace='patient_management_app')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)