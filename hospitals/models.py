from django.db import models
from accounts.models import CustomUser
# Create your models here.


class Hospital(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name
