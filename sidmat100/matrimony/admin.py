from django.contrib import admin
from .models import *






from .models import PersonalDetails, FamilyDetails, EducationalDetails, EmploymentDetails, LocationDetails,Hobby

@admin.register(PersonalDetails)
class PersonalDetailsAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'gender', 'date_of_birth', 'marital_status']  # Customize as needed

@admin.register(FamilyDetails)
class FamilyDetailsAdmin(admin.ModelAdmin):
    list_display = ['user', 'father_name', 'mother_name', 'number_of_siblings', 'father_occupation', 'mother_occupation']  # Customize as needed

@admin.register(EducationalDetails)
class EducationalDetailsAdmin(admin.ModelAdmin):
    list_display = ['user', 'highest_qualification', 'ug_degree', 'pg_degree', 'grad_year', 'college_institution']  # Customize as needed

@admin.register(EmploymentDetails)
class EmploymentDetailsAdmin(admin.ModelAdmin):
    list_display = ['user', 'employment_status', 'occupation', 'employerof', 'annual_income', 'industry']  # Customize as needed

@admin.register(LocationDetails)
class LocationDetailsAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_city', 'current_state', 'current_pin_code', 'willing_to_move']  # Customize as needed


admin.site.register(Hobby)
