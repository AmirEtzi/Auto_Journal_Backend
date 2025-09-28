from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from trades.views import TradeViewSet, register_view, login_view, logout_view, me_view

router = DefaultRouter()
router.register(r'trades', TradeViewSet, basename='trade')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/register/', register_view, name='register'),
    path('api/auth/login/', login_view, name='login'),
    path('api/auth/logout/', logout_view, name='logout'),
    path('api/auth/me/', me_view, name='me'),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
