from django.urls import path
from .views import (
    DocumentListCreateView,
    DocumentRetrieveUpdateDeleteView,
    SecureDocumentView
)

urlpatterns = [
    path('patients/<int:patient_id>/documents/', DocumentListCreateView.as_view(), name='document-list-create'),
    path('documents/<int:pk>/', DocumentRetrieveUpdateDeleteView.as_view(), name='document-detail'),
    path('documents/<int:pk>/view/', SecureDocumentView.as_view(), name='secure-document-view'),
]
