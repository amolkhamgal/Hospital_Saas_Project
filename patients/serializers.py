from rest_framework import serializers
from .models import Patient
from hospitals.models import Hospital

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'user', 'name', 'hospital']
