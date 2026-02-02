from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

def home_view(request):
    return HttpResponse("""
    <h1>🏥 Orthocare Backend API - PRODUCTION LIVE ✅</h1>
    <p><strong>Railway + PostgreSQL + Django Admin</strong></p>
    <ul>
        <li><a href="/admin/">→ Django Admin Panel</a></li>
        <li><a href="/api/accounts/">→ Accounts API</a></li>
        <li><a href="/api/patients/">→ Patients API</a></li>
        <li><a href="/api/visits/">→ Visits API</a></li>
        <li><a href="/health/">→ Health Check</a></li>
    </ul>
    """, content_type="text/html")

urlpatterns = [
    path('', home_view, name='home'),
    path('health/', lambda request: HttpResponse("OK", status=200), name='health'),
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/patients/', include('patients.urls')),
    path('api/visits/', include('visits.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
