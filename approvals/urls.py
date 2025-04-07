from django.urls import path
from .views import ApprovalListCreateView, ApprovalUpdateView

urlpatterns = [
    path('patients/<int:patient_id>/approvals/', ApprovalListCreateView.as_view(), name='approval-list-create'),
    path('patients/<int:patient_id>/approvals/<int:approval_id>/', ApprovalUpdateView.as_view(), name='approval-update'),
]
