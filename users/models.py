# smart_electric_service/users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'কাস্টমার'),
        ('technician', 'টেকনিশিয়ান'),
    )
    
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer', verbose_name='ইউজার টাইপ')
    
    # আপনি আপনার প্রয়োজন অনুযায়ী আরও ফিল্ড যোগ করতে পারেন

    # ensure that email is unique or phone_number is unique
    class Meta:
        verbose_name = "User" # এটি আপনার মডেলের একক নাম
        verbose_name_plural = "Users" # এটি আপনার মডেলের বহু নাম

    def __str__(self):
        return self.username