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
