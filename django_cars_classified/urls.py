from django.contrib import admin
from django.urls import path

from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
      path('admin/', admin.site.urls),
      path('api/v1/comments/', include(("comments.api.urls", 'comments-api'), namespace='comments-api')),
      path('api/v1/accounts/', include(('restaccounts.urls', 'restaccounts'), namespace='restaccounts')),
      path('api/v1/post/', include(('anar_ads.urls', 'anar_ads'), namespace='anar_ads')),
      path('api/v1/rest-auth/', include('rest_auth.urls')),
      path('api/v1/rest-auth/register/', include('rest_auth.registration.urls')),
      path('api/v1/api-token-auth/', obtain_jwt_token),
      path('api/v1/api-token-refresh/', refresh_jwt_token),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
