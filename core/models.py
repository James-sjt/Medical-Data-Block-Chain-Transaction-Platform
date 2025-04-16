from django.db import models
from django.contrib.auth.models import User

class DataFile(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='uploads/')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    current_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_files')
    upload_time = models.DateTimeField(auto_now_add=True)
    is_for_sale = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

class Transaction(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    datafile = models.ForeignKey(DataFile, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)