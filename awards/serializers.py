from rest_framework import serializers
from .models import Award



class AwardsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Award
        fields = ['title', 'year', 'society']
        read_only_fields = fields