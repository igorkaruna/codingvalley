from django.contrib import admin
from django.conf import settings
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('watchlists/', include('watchlists.urls')),
    path('notifications/', include('notifications.urls')),
    path('', include('users.urls')),
    path('', include('reviews.urls')),
    path('', include('discussions.urls')),
]

if settings.DEBUG:
    urlpatterns += [
            path('__debug__/', include('debug_toolbar.urls')),
    ]
