from django.urls import path

from teacher.views import (
    CloudinfraListView,
    CloudinfraCreateView,
    CloudinfraDeleteView,
    CloudinfraDetailView,
    RouterCreateView,
    NetworkCreateView,
    ServerCreateView,
    buildInfra
)

app_name = 'teacher'

urlpatterns = [
    path('<int:pk>/infra/', CloudinfraListView.as_view(), name='infra-list'),
    path('<int:pk>/infra/create/', CloudinfraCreateView.as_view(), name='infra-create'),
    path('<int:pk>/infra/<int:pk2>/', CloudinfraDetailView.as_view(), name='infra-detail'),
    path('<int:pk>/infra/<int:pk2>/delete/', CloudinfraDeleteView.as_view(), name='infra-delete'),

    path('<int:pk>/infra/<int:pk2>/router/create/', RouterCreateView.as_view(), name='router-create'),
    path('<int:pk>/infra/<int:pk2>/network/create/', NetworkCreateView.as_view(), name='network-create'),
    path('<int:pk>/infra/<int:pk2>/server/create/', ServerCreateView.as_view(), name='server-create'),

    path('<int:pk>/infra/<int:pk2>/build/', buildInfra, name='build-infra'),
    
]

