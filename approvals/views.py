from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import PatientApproval
from .serializers import PatientApprovalSerializer

class ApprovalListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientApprovalSerializer

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return PatientApproval.objects.filter(patient_id=patient_id)

    def perform_create(self, serializer):
        serializer.save(patient_id=self.kwargs['patient_id'])

class ApprovalUpdateView(generics.UpdateAPIView):
    queryset = PatientApproval.objects.all()
    serializer_class = PatientApprovalSerializer
    lookup_url_kwarg = 'approval_id'
