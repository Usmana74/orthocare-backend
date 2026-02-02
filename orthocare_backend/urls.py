from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ROOT - Simple API status
    path('', lambda request: HttpResponse('Orthocare Backend API - LIVE ✅')),
    
    # DEFAULT DJANGO ADMIN 
    path('admin/', admin.site.urls),
    
    # YOUR API ROUTES
    path('api/accounts/', include('accounts.urls')),
    path('api/patients/', include('patients.urls')),
    path('api/visits/', include('visits.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
