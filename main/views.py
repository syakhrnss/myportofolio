import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied        

from main.models import Experience, Project
from main.forms import ProjectForm, ExperienceForm


def show_main(request):
    featured_experiences = Experience.objects.filter(
        is_featured=True
    ).order_by("display_order")
    featured_projects = Project.objects.all()[:3]

    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')

    context = {
        "name": "Arsya",
        "full_name": "Arsya Khairunissa Budiman",
        "npm": "2506544076",
        "study_program": "Information Systems",
        "bio": (
            "I am Arsya Khairunissa Budiman, an undergraduate Information Systems student at Universitas Indonesia."
            "Passionate about exploring data, technology, and innovation to solve real-world problems. "
        ),
        "featured_experiences": featured_experiences,
        "featured_projects": featured_projects,
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    json_response = get_experiences_json(request)

    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )

    experiences = [experience.object for experience in experiences]

    experiences.sort(
        key=lambda experience: experience.started_at,
        reverse=True,
    )

    title_query = request.GET.get("title", "").strip()
    category_query = request.GET.get("category", "").strip()


    context = {
        "name": "Arsya",
        "full_name": "Arsya Khairunissa Budiman",
        "experience_list": experiences,
        "title_query": title_query,
    }
    return render(request, "experience.html", context)

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]

    title_query = request.GET.get("title", "").strip()

    sort_query = request.GET.get("sort", "")

    if sort_query == "stars":
        projects.sort(
            key=lambda project: project.starred_by.count(),
            reverse=True,
        )

    is_editor = request.user.groups.filter(name="Editor").exists()

    context = {
        "name": "Arsya",
        "full_name": "Arsya Khairunissa Budiman",
        "project_list": projects,
        "title_query": title_query,
        "is_editor": is_editor,
    }

    return render(request, "projects.html", context)

@login_required(login_url="/login")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Arsya",
        "form": form,
    }
    return render(request, "projects_form.html", context)

@login_required(login_url="/login/")
def edit_project(request, project_id):
    is_editor = request.user.groups.filter(name="Editor").exists()

    if not request.user.is_superuser and not is_editor:
        raise PermissionDenied
    
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Project berhasil diperbarui!")
        return redirect("main:show_projects")

    context = {
        "name": "Arsya",
        "form": form,
        "project": project,
    }

    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

@login_required(login_url="/login")
def delete_project(request, project_id):
    if not request.user.is_superuser:
            raise PermissionDenied
    
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Arsya",
        "form": form,
    }

    return render(request, "experience_form.html", context)

def edit_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Arsya",
        "form": form,
        "experience": experience,
    }

    return render(request, "experience_form.html", context)

def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")

    return redirect("main:show_experience")

def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    category_query = request.GET.get("category", "").strip()

    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(
            title__icontains=title_query
        )

    if category_query:
        experiences = experiences.filter(
            category=category_query
        )

    experiences_json = serializers.serialize(
        "json",
        experiences,
    )

    return HttpResponse(
        experiences_json,
        content_type="application/json",
    )

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Arsya",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main::show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Arsya",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Arsya",
        "form": form,
    }
    return render(request, "login.html", context)

# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star
@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")