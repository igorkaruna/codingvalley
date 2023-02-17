from django.contrib import admin
from django.conf import settings
from django.urls import path, include

from base.yasg import urlpatterns as doc_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('notifications/', include('notifications.urls')),
    path('', include('users.urls')),
    path('watchlists/', include('watchlists.urls')),
    path('', include('discussions.urls')),
    path('', include('reviews.urls')),
]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += [
            path('__debug__/', include('debug_toolbar.urls')),
    ]
