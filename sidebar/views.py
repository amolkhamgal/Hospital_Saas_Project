from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import SidebarItem
from .serializers import SidebarItemSerializer

class SidebarListView(generics.ListAPIView):
    serializer_class = SidebarItemSerializer

    def get_queryset(self):
        # You could add actual permission logic here
        return SidebarItem.objects.all().order_by('order')
