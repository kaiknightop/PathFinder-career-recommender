from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CareerPath(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, help_text="FontAwesome or Lucide icon class name")

    required_degree = models.CharField(max_length=100, blank=True, null=True)
    required_skills = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    average_salary = models.CharField(max_length=50, blank=True, null=True)
    growth_potential = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.title
    

class JobSearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    results = models.JSONField()
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.query}"
    

