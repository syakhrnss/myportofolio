from django.forms import ModelForm, TextInput, Textarea

from main.models import Project, Experience


class ProjectForm(ModelForm):
    class Meta:
        model = Project

        fields = [
            "title",
            "subtitle",
            "image",
            "description",
        ]

        labels = {
            "title": "Nama Proyek",
            "subtitle": "Subtitle Proyek",
            "image": "Gambar Proyek",
            "description": "Deskripsi Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "subtitle": TextInput(
                attrs={
                    "placeholder": "Personal Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "image": TextInput(
                attrs={
                    "placeholder": "img/vinix.png",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
        }

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
            "role",
            "is_featured",
            "display_order",
        ]