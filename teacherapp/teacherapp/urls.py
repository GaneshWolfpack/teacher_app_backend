from django.contrib import admin
from django.urls import path,include
from dj_rest_auth.views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url
schema_view = get_schema_view(
   openapi.Info(
      title="Teacher API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('register/', include('dj_rest_auth.registration.urls')),
    path("user/",include("user.urls")),
    path("login/",LoginView.as_view(),name="login"),
    path("password/reset/",PasswordResetView.as_view(),name="forgot_password"),
    path("password/change/",PasswordChangeView.as_view(),name="change_password"),
    path("logout/",LogoutView.as_view(),name="logout"),
    path("account/", include("allauth.urls"))

]
