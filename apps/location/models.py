# smart_electric_service/location/models.py

from django.db import models

class Division(models.Model):
    name = models.CharField(max_length=100, unique=True)
    bn_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.bn_name if self.bn_name else self.name
    
    class Meta:
        verbose_name_plural = "Divisions"

class District(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100)
    bn_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.bn_name if self.bn_name else self.name
    
    class Meta:
        verbose_name_plural = "Districts"

class Upazila(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='upazilas')
    name = models.CharField(max_length=100)
    bn_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.bn_name if self.bn_name else self.name
    
    class Meta:
        verbose_name_plural = "Upazilas"

class Union(models.Model):
    upazila = models.ForeignKey(Upazila, on_delete=models.CASCADE, related_name='unions')
    name = models.CharField(max_length=100)
    bn_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.bn_name if self.bn_name else self.name
    
    class Meta:
        verbose_name_plural = "Unions"

class Village(models.Model):
    union = models.ForeignKey(Union, on_delete=models.CASCADE, related_name='villages')
    name = models.CharField(max_length=100)
    bn_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.bn_name if self.bn_name else self.name
    
    class Meta:
        verbose_name_plural = "Villages"