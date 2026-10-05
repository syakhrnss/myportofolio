from django.forms import ModelForm, TextInput, Textarea, Select, URLInput, DateInput, CheckboxInput, NumberInput
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

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

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()

        if not title:
            raise ValidationError(
                "Nama proyek tidak boleh hanya berisi tag HTML."
            )

        return title

    def clean_subtitle(self):
        return strip_tags(self.cleaned_data["subtitle"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

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
            "started_at": DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                },
            ),
            "ended_at": DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                },
            ),
        }
    
    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()

        if not title:
            raise ValidationError(
                "Nama pengalaman tidak boleh hanya berisi tag HTML."
            )

        return title

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()

        if not description:
            raise ValidationError(
                "Deskripsi tidak boleh hanya berisi tag HTML."
            )

        return description

    def clean_role(self):
        role = strip_tags(self.cleaned_data["role"]).strip()

        if not role:
            raise ValidationError(
                "Peran tidak boleh hanya berisi tag HTML."
            )

        return role

    def clean(self):
        cleaned_data = super().clean()
        started_at = cleaned_data.get("started_at")
        ended_at = cleaned_data.get("ended_at")

        if started_at and ended_at and ended_at < started_at:
            self.add_error(
                "ended_at",
                "Tanggal selesai tidak boleh lebih awal dari tanggal mulai.",
            )

        return cleaned_data