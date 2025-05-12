from django.db import models
from django.contrib.auth import get_user_model

class BasicCondition(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='basic_condition')
    diagnosis_date = models.DateField(null=True, blank=True)
    first_attack_date = models.DateField(null=True, blank=True)
    attack_frequency = models.CharField(max_length=50, blank=True)
    pain_level = models.FloatField(null=True, blank=True)
    gout_type = models.CharField(max_length=50, blank=True)
    drinking_history = models.CharField(max_length=50, blank=True)
    drink_soda = models.BooleanField(default=False)
    soda_frequency = models.CharField(max_length=50, blank=True)
    limit_purine = models.BooleanField(default=False)
    limit_purine_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'basic_condition'

class LimitFood(models.Model):
    basic_condition = models.ForeignKey(BasicCondition, on_delete=models.CASCADE, related_name='limit_foods')
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'limit_food'
        unique_together = ['basic_condition', 'name']

class Complication(models.Model):
    basic_condition = models.ForeignKey(BasicCondition, on_delete=models.CASCADE, related_name='complications')
    name = models.CharField(max_length=100)
    diagnosis_date = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'complication'
        unique_together = ['basic_condition', 'name']

class Medicine(models.Model):
    basic_condition = models.ForeignKey(BasicCondition, on_delete=models.CASCADE, related_name='medicines')
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'medicine'

class PatientConditionView(models.Model):
    """
    This is a database view model that represents the patient_condition_view.
    It's a read-only model that combines basic condition with related data.
    """
    condition_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    user_phone = models.CharField(max_length=11)
    diagnosis_date = models.DateField(null=True, blank=True)
    first_attack_date = models.DateField(null=True, blank=True)
    attack_frequency = models.CharField(max_length=50, blank=True)
    pain_level = models.FloatField(null=True, blank=True)
    gout_type = models.CharField(max_length=50, blank=True)
    drinking_history = models.CharField(max_length=50, blank=True)
    drink_soda = models.BooleanField(default=False)
    soda_frequency = models.CharField(max_length=50, blank=True)
    limit_purine = models.BooleanField(default=False)
    limit_purine_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
    # JSON fields for related data
    limit_foods = models.JSONField(default=list)
    complications = models.JSONField(default=list)
    medicines = models.JSONField(default=list)
    
    class Meta:
        managed = False  # This model is a database view, not a real table
        db_table = 'patient_condition_view'
        verbose_name = '患者病情视图'
        verbose_name_plural = '患者病情视图'
