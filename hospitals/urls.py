from django.urls import path
from .views import HospitalListCreateView, HospitalRetrieveUpdateDeleteView

urlpatterns = [
    path('', HospitalListCreateView.as_view(), name='hospital-list-create'),
    path('<int:pk>/', HospitalRetrieveUpdateDeleteView.as_view(), name='hospital-detail'),
]
