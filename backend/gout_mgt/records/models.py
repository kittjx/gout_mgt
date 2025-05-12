from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='records')
    record_type = models.CharField(max_length=50)  # weight, mainFood, etc.
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

class WeightRecord(models.Model):
    record = models.OneToOneField(Record, on_delete=models.CASCADE, primary_key=True, related_name='weight_data')
    value = models.DecimalField(max_digits=5, decimal_places=2)

class MainFoodRecord(models.Model):
    record = models.OneToOneField(Record, on_delete=models.CASCADE, primary_key=True, related_name='main_food_data')
    name = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)

class WaterIntakeRecord(models.Model):
    record = models.OneToOneField(Record, on_delete=models.CASCADE, primary_key=True, related_name='water_intake_data')
    amount = models.CharField(max_length=100)

class PurineFoodRecord(models.Model):
    record = models.OneToOneField(Record, on_delete=models.CASCADE, primary_key=True, related_name='purine_food_data')
    type = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)

class UricAcidRecord(models.Model):
    record = models.OneToOneField(Record, on_delete=models.CASCADE, primary_key=True, related_name='uric_acid_data')
    value = models.CharField(max_length=100)
    method = models.CharField(max_length=20)

class UrinePHRecord(models.Model):
    record = models.OneToOneField(Record, on_delete=models.CASCADE, primary_key=True, related_name='urine_ph_data')
    value = models.CharField(max_length=100)

class LiverFunctionRecord(models.Model):
    record = models.OneToOneField(Record, on_delete=models.CASCADE, primary_key=True, related_name='liver_function_data')
    value = models.CharField(max_length=100)

# Adding the missing models
class KidneyFunctionRecord(models.Model):
    record = models.OneToOneField(Record, on_delete=models.CASCADE, primary_key=True, related_name='kidney_function_data')
    value = models.CharField(max_length=100)

class BloodSugarRecord(models.Model):
    record = models.OneToOneField(Record, on_delete=models.CASCADE, primary_key=True, related_name='blood_sugar_data')
    value = models.CharField(max_length=100)

class BloodPressureRecord(models.Model):
    record = models.OneToOneField(Record, on_delete=models.CASCADE, primary_key=True, related_name='blood_pressure_data')
    value = models.CharField(max_length=100)

class BloodLipidRecord(models.Model):
    record = models.OneToOneField(Record, on_delete=models.CASCADE, primary_key=True, related_name='blood_lipid_data')
    value = models.CharField(max_length=100)

class AttackRecord(models.Model):
    record = models.OneToOneField(Record, on_delete=models.CASCADE, primary_key=True, related_name='attack_data')
    pain_score = models.IntegerField()  # 疼痛评分 1-10
    duration = models.DecimalField(max_digits=5, decimal_places=2)

class TophiRecord(models.Model):
    record = models.OneToOneField(Record, on_delete=models.CASCADE, primary_key=True, related_name='tophi_data')
    location = models.CharField(max_length=100)  # 部位
    size = models.CharField(max_length=50)  # 大小

class SurgeryRecord(models.Model):
    record = models.OneToOneField(Record, on_delete=models.CASCADE, primary_key=True, related_name='surgery_data')
    location = models.CharField(max_length=100, blank=True, null=True)  # 部位
    notes = models.TextField(blank=True, null=True)  # 备注

class JointFunctionRecord(models.Model):
    record = models.OneToOneField(Record, on_delete=models.CASCADE, primary_key=True, related_name='joint_function_data')
    joint = models.CharField(max_length=50)  # 关节
    description = models.CharField(max_length=50)  # 描述

class UserRecordsView(models.Model):
    """
    This is a database view model that represents the user_records_view.
    It's a read-only model that combines all record types for easier querying.
    """
    record_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    user_phone = models.CharField(max_length=11)
    record_type = models.CharField(max_length=50)
    date = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
    # Weight data
    weight_value = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    
    # Main food data
    main_food_name = models.CharField(max_length=100, null=True)
    main_food_amount = models.CharField(max_length=100, null=True)
    
    # Water intake data
    water_intake_amount = models.CharField(max_length=100, null=True)
    
    # Purine food data
    purine_food_type = models.CharField(max_length=100, null=True)
    purine_food_amount = models.CharField(max_length=100, null=True)
    
    # Uric acid data
    uric_acid_value = models.CharField(max_length=100, null=True)
    uric_acid_method = models.CharField(max_length=20, null=True)
    
    # Urine pH data
    urine_ph_value = models.CharField(max_length=100, null=True)
    
    # Liver function data
    liver_function_value = models.CharField(max_length=100, null=True)
    
    # Kidney function data
    kidney_function_value = models.CharField(max_length=100, null=True)
    
    # Blood sugar data
    blood_sugar_value = models.CharField(max_length=100, null=True)
    
    # Blood pressure data
    blood_pressure_value = models.CharField(max_length=100, null=True)
    
    # Blood lipid data
    blood_lipid_value = models.CharField(max_length=100, null=True)
    
    # Attack data
    attack_pain_score = models.IntegerField(null=True)
    attack_duration = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    
    # Tophi data
    tophi_location = models.CharField(max_length=100, null=True)
    tophi_size = models.CharField(max_length=50, null=True)
    
    # Surgery data
    surgery_location = models.CharField(max_length=100, null=True)
    surgery_notes = models.TextField(null=True)
    
    # Joint function data
    joint_function_joint = models.CharField(max_length=50, null=True)
    joint_function_description = models.CharField(max_length=50, null=True)
    
    class Meta:
        managed = False  # This model is a database view, not a real table
        db_table = 'user_records_view'
        verbose_name = '用户记录视图'
        verbose_name_plural = '用户记录视图'
