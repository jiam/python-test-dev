from django.contrib import admin
from django.urls import path, include
from httpapitest import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('httpapitest/', include('httpapitest.urls')),
    
]