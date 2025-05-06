from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='records')
    record_type = models.CharField(max_length=50)  # weight, mainFood, etc.
    date = models.DateTimeField()
    data = models.JSONField()  # Store the record data as JSON
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']  # Newest first
