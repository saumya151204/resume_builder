from django.db import models
from django.contrib.auth.models import User

class Personal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    
# Main Resume
class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    
    template = models.CharField(max_length=50, default='template1')
    mode = models.CharField(
        max_length=10,
        choices=[('simple', 'Simple'), ('step', 'Step')],
        default='simple'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Personal Info (One-to-One)
class PersonalInfo(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE)
    
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    
    summary = models.TextField()

    def __str__(self):
        return self.full_name


# Education (Multiple)
class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    
    degree = models.CharField(max_length=100)
    college = models.CharField(max_length=200)
    year = models.CharField(max_length=10)

    def __str__(self):
        return self.degree


# Experience (Multiple)
class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    
    job_title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=50)

    def __str__(self):
        return self.job_title


# Skills (Multiple)
class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Projects (Multiple)
class Project(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title
    

class ContactQuery(models.Model):
    QUERY_TYPES = [
        ('Technical Issue', 'Technical Issue'),
        ('Resume Help', 'Resume Help'),
        ('Account Issue', 'Account Issue'),
        ('Feature Request', 'Feature Request'),
        ('Other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    query_type = models.CharField(max_length=50, choices=QUERY_TYPES, default='Other')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"