from django.shortcuts import render

from main.models import Experience, Project


def show_main(request):
    featured_experiences = Experience.objects.filter(
        is_featured=True
    ).order_by("display_order")

    context = {
        "name": "Arsya",
        "npm": "2506544076",
        "study_program": "Information Systems",
        "bio": (
            "I am Arsya Khairunissa Budiman, an undergraduate Information Systems student at Universitas Indonesia."
            "Passionate about exploring data, technology, and innovation to solve real-world problems. "
        ),
        "featured_experiences": featured_experiences,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Arsya",
        "experience_list": Experience.objects.all().order_by("-started_at"),
    }
    return render(request, "experience.html", context)

def show_projects(request):
    project_list = Project.objects.all()

    context = {
        "name": "Arsya",
        "project_list": project_list,
    }

    return render(request, "projects.html", context)