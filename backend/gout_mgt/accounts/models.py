from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('Phone number is required')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=11, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return self.phone


import random
from django.utils import timezone
from datetime import timedelta

class VerificationCode(models.Model):
    phone = models.CharField(max_length=11)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @classmethod
    def generate_code(cls, phone):
        # Delete existing codes for this phone
        cls.objects.filter(phone=phone).delete()
        
        # Generate a new 6-digit code
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        verification = cls.objects.create(phone=phone, code=code)
        return code
    
    @classmethod
    def verify_code(cls, phone, code):
        # Check if code exists and is valid (within 10 minutes)
        valid_time = timezone.now() - timedelta(minutes=10)
        try:
            verification = cls.objects.get(
                phone=phone,
                code=code,
                created_at__gte=valid_time
            )
            verification.delete()  # Use once and delete
            return True
        except cls.DoesNotExist:
            return False