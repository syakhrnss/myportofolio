from django.forms import ModelForm, TextInput, Textarea, Select, URLInput, DateInput, CheckboxInput, NumberInput

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
            "image": URLInput(
                attrs={
                    "placeholder": "https://example.com/image.jpg",
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

        labels = {
            "title": "Nama Pengalaman",
            "description": "Deskripsi",
            "category": "Kategori",
            "thumbnail": "Thumbnail",
            "started_at": "Mulai",
            "ended_at": "Selesai",
            "role": "Peran",
            "is_featured": "Tampilkan di Home",
            "display_order": "Urutan Tampilan",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "PT Hiden Intelligence",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pengalamanmu",
                    "rows": 4,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://example.com/image.jpg",
                }
            ),
            "started_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "ended_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "role": TextInput(
                attrs={
                    "placeholder": "Data Analyst Intern",
                    "maxlength": 100,
                }
            ),
            "is_featured": CheckboxInput(
                attrs={
                    "class": "form-checkbox",
                }
            ),
            "display_order": NumberInput(
                attrs={
                    "class": "form-input",
                    "min": 0,
                }
            ),
        }