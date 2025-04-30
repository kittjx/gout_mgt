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
    limit_foods = models.JSONField(default=list, blank=True)
    complications = models.JSONField(default=list, blank=True)
    complication_dates = models.JSONField(default=dict, blank=True)
    medicines = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'basic_condition'
