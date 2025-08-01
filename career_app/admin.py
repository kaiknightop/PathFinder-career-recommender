from django.contrib import admin
from .models import CareerPath
# Register your models here.

@admin.register(CareerPath)
class CareerPathAdmin(admin.ModelAdmin):
    list_display = ('title', 'required_degree', 'average_salary', 'growth_potential')
    search_fields = ('title', 'required_skills', 'certifications')