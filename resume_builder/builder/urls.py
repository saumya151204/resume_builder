from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('dashboard/', views.dashboard, name='dashboard'), 
    
    path('register/', views.register, name='register'),
    path('create/', views.create_resume, name='create_resume'),
    path('contact/', views.contact, name='contact'),
    path('donate/', views.donate, name='donate'),
    
    path('<int:resume_id>/template/', views.select_template, name='select_template'),
    path('<int:resume_id>/mode/', views.select_mode, name='select_mode'),
    path('<int:resume_id>/personal/', views.personal_info, name='personal_info'),
    path('<int:resume_id>/education/', views.education, name='education'),
    path('<int:resume_id>/experience/', views.experience, name='experience'),
    path('<int:resume_id>/skills/', views.skills, name='skills'),
    path('<int:resume_id>/projects/', views.projects, name='projects'),
    path('<int:resume_id>/preview/', views.preview, name='preview'),
    path('<int:resume_id>/delete/', views.delete_resume, name='delete_resume'),
    
    path('<int:id>/pdf/', views.download_pdf, name='download_pdf'),
]