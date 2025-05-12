from rest_framework import serializers
from .models import (
    Record, WeightRecord, MainFoodRecord, WaterIntakeRecord, 
    PurineFoodRecord, UricAcidRecord, UrinePHRecord, LiverFunctionRecord,
    KidneyFunctionRecord, BloodSugarRecord, BloodPressureRecord, BloodLipidRecord,
    AttackRecord, TophiRecord, SurgeryRecord, JointFunctionRecord, UserRecordsView
)

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['id', 'record_type', 'date', 'created_at', 'updated_at']

class WeightRecordSerializer(serializers.ModelSerializer):
    record_id = serializers.IntegerField(source='record.id', read_only=True)
    date = serializers.DateTimeField(source='record.date')
    
    class Meta:
        model = WeightRecord
        fields = ['record_id', 'date', 'value']

class MainFoodRecordSerializer(serializers.ModelSerializer):
    record_id = serializers.IntegerField(source='record.id', read_only=True)
    date = serializers.DateTimeField(source='record.date')
    
    class Meta:
        model = MainFoodRecord
        fields = ['record_id', 'date', 'name', 'amount']

class WaterIntakeRecordSerializer(serializers.ModelSerializer):
    record_id = serializers.IntegerField(source='record.id', read_only=True)
    date = serializers.DateTimeField(source='record.date')
    
    class Meta:
        model = WaterIntakeRecord
        fields = ['record_id', 'date', 'amount']

class PurineFoodRecordSerializer(serializers.ModelSerializer):
    record_id = serializers.IntegerField(source='record.id', read_only=True)
    date = serializers.DateTimeField(source='record.date')
    
    class Meta:
        model = PurineFoodRecord
        fields = ['record_id', 'date', 'type', 'amount']

class UricAcidRecordSerializer(serializers.ModelSerializer):
    record_id = serializers.IntegerField(source='record.id', read_only=True)
    date = serializers.DateTimeField(source='record.date')
    
    class Meta:
        model = UricAcidRecord
        fields = ['record_id', 'date', 'value', 'method']

class UrinePHRecordSerializer(serializers.ModelSerializer):
    record_id = serializers.IntegerField(source='record.id', read_only=True)
    date = serializers.DateTimeField(source='record.date')
    
    class Meta:
        model = UrinePHRecord
        fields = ['record_id', 'date', 'value']

class LiverFunctionRecordSerializer(serializers.ModelSerializer):
    record_id = serializers.IntegerField(source='record.id', read_only=True)
    date = serializers.DateTimeField(source='record.date')
    
    class Meta:
        model = LiverFunctionRecord
        fields = ['record_id', 'date', 'value']

# New serializers for the added models
class KidneyFunctionRecordSerializer(serializers.ModelSerializer):
    record_id = serializers.IntegerField(source='record.id', read_only=True)
    date = serializers.DateTimeField(source='record.date')
    
    class Meta:
        model = KidneyFunctionRecord
        fields = ['record_id', 'date', 'value']

class BloodSugarRecordSerializer(serializers.ModelSerializer):
    record_id = serializers.IntegerField(source='record.id', read_only=True)
    date = serializers.DateTimeField(source='record.date')
    
    class Meta:
        model = BloodSugarRecord
        fields = ['record_id', 'date', 'value']

class BloodPressureRecordSerializer(serializers.ModelSerializer):
    record_id = serializers.IntegerField(source='record.id', read_only=True)
    date = serializers.DateTimeField(source='record.date')
    
    class Meta:
        model = BloodPressureRecord
        fields = ['record_id', 'date', 'value']

class BloodLipidRecordSerializer(serializers.ModelSerializer):
    record_id = serializers.IntegerField(source='record.id', read_only=True)
    date = serializers.DateTimeField(source='record.date')
    
    class Meta:
        model = BloodLipidRecord
        fields = ['record_id', 'date', 'value']

class AttackRecordSerializer(serializers.ModelSerializer):
    record_id = serializers.IntegerField(source='record.id', read_only=True)
    date = serializers.DateTimeField(source='record.date')
    
    class Meta:
        model = AttackRecord
        fields = ['record_id', 'date', 'pain_score', 'duration']

class TophiRecordSerializer(serializers.ModelSerializer):
    record_id = serializers.IntegerField(source='record.id', read_only=True)
    date = serializers.DateTimeField(source='record.date')
    
    class Meta:
        model = TophiRecord
        fields = ['record_id', 'date', 'location', 'size']

class SurgeryRecordSerializer(serializers.ModelSerializer):
    record_id = serializers.IntegerField(source='record.id', read_only=True)
    date = serializers.DateTimeField(source='record.date')
    
    class Meta:
        model = SurgeryRecord
        fields = ['record_id', 'date', 'location', 'notes']

class JointFunctionRecordSerializer(serializers.ModelSerializer):
    record_id = serializers.IntegerField(source='record.id', read_only=True)
    date = serializers.DateTimeField(source='record.date')
    
    class Meta:
        model = JointFunctionRecord
        fields = ['record_id', 'date', 'joint', 'description']

class UserRecordsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRecordsView
        fields = '__all__'
