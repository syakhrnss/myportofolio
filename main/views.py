import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied  
from django.http import JsonResponse
from django.views.decorators.http import require_POST      

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

    title_query = request.GET.get("title", "").strip()
    category_query = request.GET.get("category", "").strip()
    sort_query = request.GET.get("sort", "")

    if sort_query == "stars":
        experiences.sort(
            key=lambda project: project.starred_by.count(),
            reverse=True,
        )
    else:
        experiences.sort(
        key=lambda experience: experience.started_at,
        reverse=True,
        )

    is_editor = request.user.groups.filter(name="Editor").exists()

    context = {
        "name": "Arsya",
        "full_name": "Arsya Khairunissa Budiman",
        "experience_list": experiences,
        "title_query": title_query,
        "category_query" : category_query,
        "sort_query" : sort_query,
        "is_editor": is_editor,
    }
    return render(request, "experience.html", context)

def show_projects(request):
    title_query = request.GET.get("title", "").strip()
    sort_query = request.GET.get("sort", "")

    is_editor = request.user.groups.filter(name="Editor").exists()

    context = {
        "name": "Arsya",
        "full_name": "Arsya Khairunissa Budiman",
        "title_query": title_query,
        "sort_query": sort_query,
        "is_editor": is_editor,
        "form": ProjectForm(),
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
    sort_query = request.GET.get("sort", "")

    projects = Project.objects.prefetch_related("starred_by").all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    if sort_query == "stars":
        projects = sorted(
            projects,
            key=lambda project: project.starred_by.count(),
            reverse=True,
        )

    data = []

    for project in projects:
        starred_users = project.starred_by.all()

        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )

        starred_by_names = ", ".join(
            [u.username for u in starred_users]
        )

        data.append({
            "model": "main.project",
            "pk": project.id,
            "fields": {
                "title": project.title,
                "subtitle": project.subtitle,
                "image": project.image,
                "description": project.description,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
                "starred_by": list(
                    project.starred_by.values_list("id", flat=True)
                ),
            }
        })

    return JsonResponse(data, safe=False)

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

@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
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

@login_required(login_url="/login/")
def edit_experience(request, experience_id):
    is_editor = request.user.groups.filter(name="Editor").exists()

    if not request.user.is_superuser and not is_editor:
        raise PermissionDenied
    
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

@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
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
        response = redirect("main:show_main")
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

@login_required(login_url="/login/")
def toggle_experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")

@require_POST
def create_project_ajax(request):
    print(">>> MASUK CREATE PROJECT AJAX")
    print(">>> POST:", request.POST)

    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    is_valid = form.is_valid()

    print(">>> FORM VALID:", is_valid)
    print(">>> FORM ERRORS:", form.errors)

    if is_valid:
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse(
        {"errors": form.errors.get_json_data()},
        status=400,
    )