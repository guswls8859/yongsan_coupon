"""
URL configuration for coopon_send project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from main_content import views as main_view

urlpatterns = [
    # path('', main_view.main_page, name='main_page'),
    # path('clear', main_view.clean_phone_numbers, name='clean_phone_numbers'),
    # path('wndqhrghkrdls', main_view.wndqhrghkrdls, name='wndqhrghkrdls'),
    # path('excel_make', main_view.excel_make, name='excel_make'),
    # path('generate_unique_numbers', main_view.generate_unique_numbers, name='generate_unique_numbers'),
    # path('ch_phone', main_view.phone_num_ch, name='clean_phone_numbers'),
    path('coopon/<str:coopon_id>', main_view.coopon, name='coopon'),
    path('coopon_use/<str:coopon_id>', main_view.coopon_use, name='coopon_use'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)