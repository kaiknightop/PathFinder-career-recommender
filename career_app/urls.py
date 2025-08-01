from django.urls import path
from . import views

urlpatterns = [
    path('', views.career_paths_list, name='career_paths_list'),
    path('career/<int:career_id>/', views.career_detail, name='career_detail'),
    path('jobs/', views.fetch_jobs, name='fetch_jobs'),
    path('job-search/', views.job_search, name='job_search'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('career-paths/', views.career_paths_view, name='career_paths'),
    path('roadmap/', views.generate_roadmap, name='generate_roadmap'),
    path('about/', views.about_view, name='about'),

]
