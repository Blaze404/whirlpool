from django.db import models

# Create your models here.


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    user_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=50, null=True)
    last_login = models.DateTimeField(auto_now=True)


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    quantity = models.CharField(max_length=20)
    current_quantity = models.CharField(max_length=20)
    description = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now=True)
    part_number = models.CharField(max_length=512, default='')
    current_non_working_quantity = models.CharField(max_length=20, default='0')


class Transactions(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    created_by = models.CharField(max_length=50)
    name = models.CharField(max_length=128)
    inventory = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=16)
    quantity = models.CharField(max_length=20)
    closed_at = models.DateTimeField(null=True)
    return_status = models.CharField(max_length=20, default='ok')
    part_number = models.CharField(max_length=512, default='')




