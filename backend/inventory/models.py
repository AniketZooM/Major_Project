from django.db import models

class Inventory(models.Model):
    part_id = models.CharField(max_length=50, unique=True)
    part_name = models.CharField(max_length=100)
    current_stock = models.IntegerField(default=0)
    reorder_point = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    
class Vehicle(models.Model):
    vehicle_no = models.CharField(max_length=20)
    vehicle_model = models.CharField(max_length=50)
    current_km_reading = models.IntegerField()

    def __str__(self):
        return f'{self.vehicle_model} - {self.vehicle_no}'


class Transaction(models.Model):
    invoice_date = models.DateField()
    job_card_date = models.DateField()
    business_partner_name = models.CharField(max_length=100)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    invoice_line_text = models.TextField()

    def __str__(self):
        return f'{self.invoice_line_text} - {self.vehicle}'

class Vehicle(models.Model):
    vehicle_no = models.CharField(max_length=20)
    vehicle_model = models.CharField(max_length=50)
    current_km_reading = models.IntegerField()

    def __str__(self):
        return f'{self.vehicle_model} - {self.vehicle_no}'


class Transaction(models.Model):
    invoice_date = models.DateField()
    job_card_date = models.DateField()
    business_partner_name = models.CharField(max_length=100)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    invoice_line_text = models.TextField()

    def __str__(self):
        return f'{self.invoice_line_text} - {self.vehicle}'

    def __str__(self):
        return f"{self.part_name} (ID: {self.part_id})"

class DemandForecast(models.Model):
    part = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    predicted_quantity = models.IntegerField()
    forecast_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Forecast for {self.part.part_name} on {self.forecast_date}"