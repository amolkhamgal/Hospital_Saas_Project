from rest_framework import serializers
from .models import SidebarItem

class SidebarItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SidebarItem
        fields = ['id', 'title', 'icon', 'link', 'order']
