from django.db import models

# Create your models here.

class SidebarItem(models.Model):
    title = models.CharField(max_length=255)
    icon = models.CharField(max_length=100, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
