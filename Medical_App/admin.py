from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Company)
admin.site.register(models.Medicine)
admin.site.register(models.MedicalDetails)
admin.site.register(models.Employee)
admin.site.register(models.Customer)
admin.site.register(models.Bill)
admin.site.register(models.EmployeeSalary)
admin.site.register(models.BillDetail)
admin.site.register(models.CustomerRequest)
admin.site.register(models.CompanyAccount)
admin.site.register(models.CompanyBank)
admin.site.register(models.EmployeeBank)