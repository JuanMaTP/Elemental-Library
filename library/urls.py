from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView

from .views import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/people/', include('person.urls')),
    path('api/books/', include('books.urls')),
    path('api/authors/', include('author.urls')),
    path('api/rentals/', include('rental.urls')),

    path('login/', MyTokenObtainPairView.as_view(), name='token-obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api-auth/', include('rest_framework.urls')),

    # OpenAPI schema and interactive docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Serve uploaded files while developing
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
