from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import FileResponse, HttpResponse
from .models import Document
from .serializers import DocumentSerializer
from approvals.models import PatientApproval

class DocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return Document.objects.filter(patient_id=patient_id)

    def perform_create(self, serializer):
        serializer.save(patient_id=self.kwargs['patient_id'])

class DocumentRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class SecureDocumentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            document = Document.objects.get(pk=pk)
            user = request.user

            if user.is_hospital:
                hospital = user.hospital
                if document.patient.hospital == hospital or \
                   PatientApproval.objects.filter(
                       patient=document.patient,
                       approved_hospital=hospital,
                       is_approved=True
                   ).exists():
                    return FileResponse(document.file.open(), content_type='application/pdf')
            elif user.is_patient and document.patient.user == user:
                return FileResponse(document.file.open(), content_type='application/pdf')

        except Document.DoesNotExist:
            return HttpResponse("Document not found.", status=404)

        return HttpResponse("Unauthorized", status=401)
