from django.db import models
from hospitals.models import Hospital
from patients.models import Patient

# Create your models here.

class PatientApproval(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    approved_hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.approved_hospital} access to {self.patient.name}"
