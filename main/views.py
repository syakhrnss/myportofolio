from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Arsya",
        "npm": "2506544076",
        "study_program": "Information Systems",
        "bio": (
            "I am Arsya Khairunissa Budiman, an undergraduate Information Systems student at Universitas Indonesia."
            "Passionate about exploring data, technology, and innovation to solve real-world problems. "
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Arsya Khairunissa Budiman",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)