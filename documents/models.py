from django.db import models
from patients.models import Patient

# Create your models here.

class Document(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    file = models.FileField(upload_to='patientDocuments/')

    def __str__(self):
        return f"Document for {self.patient.name}"
