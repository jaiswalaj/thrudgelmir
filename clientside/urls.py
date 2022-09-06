"""clientside URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include

from teacher.views import (
    CloudinfraListView,
    CloudinfraCreateView,
    CloudinfraDeleteView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('teacher/', include('teacher.urls', namespace="teacher")),

    # path('teacher/<pk>/infra/', CloudinfraListView.as_view(), name='infra-list'),
    # path('teacher/<pk>/infra/create/', CloudinfraCreateView.as_view(), name='infra-create'),
    # path('teacher/<pk>/infra/<pk2>/delete/', CloudinfraDeleteView.as_view(), name='infra-delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)