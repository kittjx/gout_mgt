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
