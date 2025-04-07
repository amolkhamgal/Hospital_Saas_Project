from rest_framework import serializers
from .models import Hospital
from accounts.models import CustomUser

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'user', 'name', 'address']
