from django.db import migrations, models


def update_experience_data(apps, schema_editor):
    Experience = apps.get_model("main", "Experience")

    roles = {
        "PT Vinix Seven Aurum": "Data Scientist Intern",
        "SIWAK-NG 2026": "Person in Charge of Business Development",
        "Indonesia Technology & Innovation (INTI) Asia Expo 2026": "Volunteer",
        "COMPFEST 18": "Staff of Data Science Academy",
        "FUKI Fasilkom UI": "Staff of Business Growth",
        "Dasar-Dasar Pemrograman 0": "Python Mentor & Staff of Business Development",
        "BETIS Fasilkom UI": "Staff of Mentor and Participant",
        "MOONZHER Olympiad Science Club": "Economics Coordinator & Tutor",
    }

    for title, role in roles.items():
        Experience.objects.filter(title=title).update(role=role)

    featured = {
        "COMPFEST 18": 1,
        "PT Vinix Seven Aurum": 2,
        "Indonesia Technology & Innovation (INTI) Asia Expo 2026": 3,
        "MOONZHER Olympiad Science Club": 4,
    }

    for title, order in featured.items():
        Experience.objects.filter(title=title).update(
            is_featured=True,
            display_order=order,
        )


def reverse_update_experience_data(apps, schema_editor):
    Experience = apps.get_model("main", "Experience")

    Experience.objects.update(
        role="",
        is_featured=False,
        display_order=0,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_seed_experience_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="experience",
            name="role",
            field=models.CharField(max_length=100, default=""),
        ),
        migrations.AddField(
            model_name="experience",
            name="is_featured",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="experience",
            name="display_order",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.RunPython(
            update_experience_data,
            reverse_update_experience_data,
        ),
    ]