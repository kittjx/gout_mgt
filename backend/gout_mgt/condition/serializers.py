from rest_framework import serializers
from .models import BasicCondition

import logging

logger = logging.getLogger(__name__)

class BasicConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicCondition
        fields = [
            'diagnosis_date',
            'first_attack_date',
            'attack_frequency',
            'pain_level',
            'gout_type',
            'drinking_history',
            'drink_soda',
            'soda_frequency',
            'limit_purine',
            'limit_purine_date',
            'limit_foods',
            'complications',
            'complication_dates',
            'medicines'
        ]
    
    def validate(self, data):
        logger.info(f"Validating data: {data}")
        return data

    def create(self, validated_data):
        logger.info(f"Creating with validated data: {validated_data}")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        logger.info(f"Updating instance with validated data: {validated_data}")
        return super().update(instance, validated_data)