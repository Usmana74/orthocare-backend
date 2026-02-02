from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

# ROOT URL - Fixes 404 on home page
def home_view(request):
    return HttpResponse("""
    <h1>🏥 Orthocare Backend API - LIVE ✅</h1>
    <p><strong>Production Deployment Successful!</strong></p>
    <ul>
        <li><a href="/admin/">Admin Panel → /admin/</a></li>
        <li><a href="/api/accounts/">Accounts API → /api/accounts/</a></li>
        <li><a href="/api/patients/">Patients API → /api/patients/</a></li>
        <li><a href="/api/visits/">Visits API → /api/visits/</a></li>
    </ul>
    <p><em>Railway + PostgreSQL + Gunicorn = 🚀 Production Ready</em></p>
    """)

urlpatterns = [
    # ROOT HOME PAGE - Shows API status
    path("", home_view, name="home"),
    
    # ADMIN
    path("admin/", admin.site.urls),
    
    # API ENDPOINTS
    path("api/accounts/", include("accounts.urls")),
    path("api/patients/", include("patients.urls")), 
    path("api/visits/", include("visits.urls")),
    
    # HEALTH CHECK
    path("health/", lambda request: HttpResponse("OK", status=200), name="health"),
]

# Media files in DEBUG mode only (local development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
