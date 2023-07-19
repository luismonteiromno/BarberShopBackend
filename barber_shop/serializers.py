from rest_framework import serializers
from .models import Company

class CompanysSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Company
        fields = '__all__'