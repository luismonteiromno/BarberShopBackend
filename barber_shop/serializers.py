from rest_framework import serializers
from .models import Company, Schedules


class CompanysSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Company
        exclude = ['business_hours', 'opening_hours']


class SchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Schedules
        fields = '__all__'
