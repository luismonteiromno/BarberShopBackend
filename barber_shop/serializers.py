from rest_framework import serializers
from .models import Company, Schedules, Days, SchedulesDays


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


class DaysSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Days
        fields = '__all__'


class SchedulesDaysSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = SchedulesDays
        fields = '__all__'
