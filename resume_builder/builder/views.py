from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib import messages
from xhtml2pdf import pisa
from .models import Resume, PersonalInfo, Education, Experience, Skill, Project
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm





def fix_template_path(template):
    if not template.startswith('template/'):
        template = f"template/{template}"
    if not template.endswith('.html'):
        template += '.html'
    return template


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF')
    return response


def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    return render(request, 'register.html', {'form': form})


def home(request):
    return render(request, 'home.html')


@login_required
def dashboard(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    if request.user.is_staff:
        return redirect('staff_dashboard')
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'resumes': resumes})

@login_required
def create_resume(request):
    resume = Resume.objects.create(user=request.user, title="My Resume")
    return redirect('select_template', resume_id=resume.id)


@login_required
def select_template(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if request.method == 'POST':
        template = request.POST.get('template')
        if not template.endswith('.html'):
            template += '.html'
        resume.template = f"template/{template}"
        resume.save()
        return redirect('select_mode', resume_id=resume.id)
    return render(request, 'select_template.html', {'resume': resume})


@login_required
def select_mode(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if request.method == 'POST':
        mode = request.POST.get('mode')
        resume.mode = mode
        resume.save()
        if mode == 'simple':
            return redirect('simple_form', resume_id=resume.id)
        else:
            return redirect('personal_info', resume_id=resume.id)
    return render(request, 'select_mode.html')

@login_required
def simple_form(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)

    if request.method == 'POST':

        PersonalInfo.objects.update_or_create(
            resume=resume,
            defaults={
                'full_name': request.POST.get('full_name'),
                'email': request.POST.get('email'),
                'phone': request.POST.get('phone'),
                'linkedin': request.POST.get('linkedin'),
                'github': request.POST.get('github'),
                'summary': request.POST.get('summary'),
            }
        )

        skills = request.POST.getlist('skills[]')
        projects = request.POST.getlist('projects[]')

        Skill.objects.filter(resume=resume).delete()
        Project.objects.filter(resume=resume).delete()

        for skill in skills:
            if skill:
                Skill.objects.create(resume=resume, name=skill)

        for project in projects:
            if project:
                Project.objects.create(resume=resume, title=project)

        return redirect('preview', resume_id=resume.id)

    return render(request, 'simple_form.html', {'resume': resume})

@login_required
def personal_info(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    instance = PersonalInfo.objects.filter(resume=resume).first()
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.resume = resume
            obj.save()
            return redirect('education', resume_id=resume.id)
    else:
        form = PersonalInfoForm(instance=instance)
    return render(request, 'personal_info.html', {'form': form})


@login_required
def education(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if request.method == 'POST':
        formset = EducationFormSet(request.POST, instance=resume)
        if formset.is_valid():
            formset.save()
            return redirect('experience', resume_id=resume.id)
    else:
        formset = EducationFormSet(instance=resume)
    return render(request, 'education.html', {'formset': formset})


@login_required
def experience(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if request.method == 'POST':
        formset = ExperienceFormSet(request.POST, instance=resume)
        if formset.is_valid():
            formset.save()
            return redirect('skills', resume_id=resume.id)
    else:
        formset = ExperienceFormSet(instance=resume)
    return render(request, 'experience.html', {'formset': formset})


@login_required
def skills(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if request.method == 'POST':
        formset = SkillFormSet(request.POST, instance=resume)
        if formset.is_valid():
            formset.save()
            return redirect('projects', resume_id=resume.id)
    else:
        formset = SkillFormSet(instance=resume)
    return render(request, 'skills.html', {'formset': formset})


@login_required
def projects(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    if request.method == 'POST':
        formset = ProjectFormSet(request.POST, instance=resume)
        if formset.is_valid():
            formset.save()
            return redirect('preview', resume_id=resume.id)
    else:
        formset = ProjectFormSet(instance=resume)
    return render(request, 'projects.html', {'formset': formset})


@login_required
def preview(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    template = fix_template_path(resume.template)
    context = {
        'resume': resume,
        'personal': PersonalInfo.objects.filter(resume=resume).first(),
        'education': Education.objects.filter(resume=resume),
        'experience': Experience.objects.filter(resume=resume),
        'skills': Skill.objects.filter(resume=resume),
        'projects': Project.objects.filter(resume=resume),
    }
    return render(request, template, context)


@login_required
def download_pdf(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    template = fix_template_path(resume.template)
    context = {
        'resume': resume,
        'personal': PersonalInfo.objects.filter(resume=resume).first(),
        'education': Education.objects.filter(resume=resume),
        'experience': Experience.objects.filter(resume=resume),
        'skills': Skill.objects.filter(resume=resume),
        'projects': Project.objects.filter(resume=resume),
        'is_pdf': True
    }
    return render_to_pdf(template, context)


@login_required
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    resume.delete()
    return redirect('dashboard')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        query_type = request.POST.get('query_type')
        subject = request.POST.get('subject')
        message_text = request.POST.get('message')

        ContactQuery.objects.create(
            name=name,
            email=email,
            query_type=query_type,
            subject=subject,
            message=message_text
        )
        messages.success(request, f'Thank you {name}! We have received your query. We will get back to you soon.')
        return redirect('contact')

    return render(request, 'contact.html')

def donate(request):
    return render(request, 'donate.html')

@login_required
def admin_dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'total_resumes': Resume.objects.count(),
        'total_queries': ContactQuery.objects.count(),
        'recent_queries': ContactQuery.objects.order_by('-created_at')[:10],
        'recent_users': User.objects.order_by('-date_joined')[:10],
        'recent_resumes': Resume.objects.order_by('-created_at')[:10],
    }
    return render(request, 'admin_dashboard.html', context)


@login_required
def staff_dashboard(request):
    if not request.user.is_staff :
        raise PermissionDenied

    context = {
        'total_users': User.objects.count(),
        'total_resumes': Resume.objects.count(),
        'total_queries': ContactQuery.objects.count(),
        'pending_queries': ContactQuery.objects.filter(status='Pending').count(),
        'resolved_queries': ContactQuery.objects.filter(status='Resolved').count(),
        'all_queries': ContactQuery.objects.order_by('-created_at'),
        'all_users': User.objects.order_by('-date_joined'),
        'all_resumes': Resume.objects.order_by('-created_at'),
    }
    return render(request, 'staff_dashboard.html', context)


@login_required
def mark_resolved(request, query_id):
    if not request.user.is_staff:
        raise PermissionDenied
    query = get_object_or_404(ContactQuery, id=query_id)
    query.status = 'Resolved'
    query.save()
    return redirect('staff_dashboard')


@login_required
def mark_pending(request, query_id):
    if not request.user.is_staff:
        raise PermissionDenied
    query = get_object_or_404(ContactQuery, id=query_id)
    query.status = 'Pending'
    query.save()
    return redirect('staff_dashboard')

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        auth_login(request, user)

        if user.is_superuser:
            return redirect('admin_dashboard')
        elif user.is_staff:
            return redirect('staff_dashboard')
        else:
            return redirect('dashboard')

    return render(request, 'login.html', {'form': form})