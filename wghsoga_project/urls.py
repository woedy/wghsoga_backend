

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/accounts/', include('accounts.api.urls', 'accounts_api')),
    path('api/projects/', include('projects.api.urls', 'projects_api')),
    path('api/news/', include('news.api.urls', 'news_api')),
    path('api/events/', include('events.api.urls', 'events_api')),
    path('api/shop/', include('shop.api.urls', 'shop_api')),

    ## path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
#
    ## path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
#
    ## path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    #path('api/token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),

]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)