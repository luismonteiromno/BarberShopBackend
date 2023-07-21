from rest_framework import serializers
from .models import AbousUs


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbousUs
        fields = '__all__'
