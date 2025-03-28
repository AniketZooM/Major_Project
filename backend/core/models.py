from django.db import models
import numpy as np

class Inventory(models.Model):
    vehicle_id = models.IntegerField()
    part_name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.part_name} - {self.quantity}"

class Vehicle(models.Model):
    vehicle_id = models.IntegerField(primary_key=True)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    mileage = models.IntegerField()

    def __str__(self):
        return f"{self.make} {self.model}"

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    part_name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction #{self.transaction_id}"

class DemandForecast(models.Model):
    forecast_id = models.AutoField(primary_key=True)
    part_name = models.CharField(max_length=200)
    forecast_date = models.DateTimeField(auto_now_add=True)
    forecast_values = models.JSONField()

    def __str__(self):
        return f"Forecast for {self.part_name}"