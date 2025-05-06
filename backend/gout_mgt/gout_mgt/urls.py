from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/patient/', include('profiles.urls')),
    path('api/condition/', include('condition.urls')),
    path('api/records/', include('records.urls')),
]
