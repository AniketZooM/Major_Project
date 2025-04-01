from django.contrib import admin
from backend.inventory.models import Vehicle, Transaction

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['vehicle_no', 'vehicle_model', 'current_km_reading']
    search_fields = ['vehicle_no', 'vehicle_model']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['invoice_date', 'job_card_date', 'business_partner_name', 'vehicle']
    search_fields = ['business_partner_name', 'vehicle__vehicle_no']
    list_filter = ['invoice_date', 'job_card_date']
