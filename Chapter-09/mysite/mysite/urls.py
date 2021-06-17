from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('auth/', include('login.urls')),
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls'))
]