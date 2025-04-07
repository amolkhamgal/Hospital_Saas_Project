from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Hospital
from .serializers import HospitalSerializer

class HospitalListCreateView(generics.ListCreateAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

class HospitalRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
