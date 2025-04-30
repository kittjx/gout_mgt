
from django.db import models
from django.conf import settings

class PatientProfile(models.Model):
    GENDER_CHOICES = (
        ('男', '男'),
        ('女', '女'),
    )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100, verbose_name='姓名')
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default='男', verbose_name='性别')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生日期')
    height = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name='身高(cm)')
    weight = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name='体重(kg)')
    phone = models.CharField(max_length=11, verbose_name='手机号码')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.user.phone}"
    
    class Meta:
        verbose_name = '患者信息'
        verbose_name_plural = '患者信息'