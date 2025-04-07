from django.urls import path
from .views import SidebarListView

urlpatterns = [
    path('', SidebarListView.as_view(), name='sidebar-list'),
]
