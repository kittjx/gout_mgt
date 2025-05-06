from rest_framework import serializers
from .models import Record

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['id', 'record_type', 'date', 'data']
        read_only_fields = ['id']