from rest_framework import serializers
from .models import PatientApproval

class PatientApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientApproval
        fields = ['id', 'patient', 'approved_hospital', 'is_approved']
