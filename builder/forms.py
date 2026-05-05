from django import forms
from .models import *
from django.forms import inlineformset_factory
from .models import Resume, Skill

# Resume Title Form
class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title']


# Personal Info Form
class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        exclude = ['resume']


# ================= FORMSETS =================

# Education
EducationFormSet = inlineformset_factory(
    Resume,
    Education,
    fields=('degree', 'college', 'year'),
    extra=1,
    can_delete=True
)

# Experience
ExperienceFormSet = inlineformset_factory(
    Resume,
    Experience,
    fields=('job_title', 'company', 'description', 'duration'),
    extra=1,
    can_delete=True
)

# Skills
SkillFormSet = inlineformset_factory(
    Resume,
    Skill,
    fields=('name',),
    extra=1,
    can_delete=True
)

# Projects
ProjectFormSet = inlineformset_factory(
    Resume,
    Project,
    fields=('title', 'description'),
    extra=1,
    can_delete=True
)