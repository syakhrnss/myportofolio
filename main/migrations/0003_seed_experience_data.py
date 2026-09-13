from django.db import migrations
from datetime import datetime


def seed_experience_data(apps, schema_editor):
    Experience = apps.get_model("main", "Experience")

    experiences = [
        {
            "title": "PT Vinix Seven Aurum",
            "description": (
                "Analyzed 65K+ e-commerce product reviews using Python and "
                "data visualization techniques. Preprocessed and explored "
                "review data to prepare datasets for machine learning and "
                "downstream analysis. Developed machine learning models for "
                "sentiment classification and customer segmentation."
            ),
            "category": "internship",
            "started_at": datetime(2026, 2, 1),
            "ended_at": datetime(2026, 6, 30),
        },
        {
            "title": "SIWAK-NG 2026",
            "description": (
                "Led the development of fundraising initiatives, including "
                "merchandise sales and other potential revenue streams."
            ),
            "category": "committee",
            "started_at": datetime(2026, 8, 1),
            "ended_at": None,
        },
        {
            "title": "Indonesia Technology & Innovation (INTI) Asia Expo 2026",
            "description": (
                "Assisted assigned speakers throughout the event, coordinating "
                "schedules, logistics, and event flow. Facilitated communication "
                "between speakers and the event committee to ensure smooth "
                "session execution."
            ),
            "category": "volunteer",
            "started_at": datetime(2026, 8, 1),
            "ended_at": datetime(2026, 8, 31),
        },
        {
            "title": "COMPFEST 18",
            "description": (
                "Invited and coordinated with mentors and guest speakers to "
                "support the execution of bootcamp sessions. Served as Liaison "
                "Officer for mentors and mentees, facilitating communication, "
                "schedules, and session logistics. Served as Master of Ceremony "
                "for two bootcamp sessions."
            ),
            "category": "committee",
            "started_at": datetime(2026, 4, 1),
            "ended_at": None,
        },
        {
            "title": "FUKI Fasilkom UI",
            "description": (
                "Explored project management and business development concepts "
                "through internal team activities."
            ),
            "category": "organization",
            "started_at": datetime(2026, 4, 1),
            "ended_at": None,
        },
        {
            "title": "Dasar-Dasar Pemrograman 0",
            "description": (
                "Mentored 5 mentees in Python programming through guided "
                "learning and problem-solving sessions. Conducted business "
                "research to identify opportunities and support program "
                "initiatives. Managed merchandise sales and supported "
                "promotional activities to drive revenue."
            ),
            "category": "committee",
            "started_at": datetime(2026, 4, 1),
            "ended_at": None,
        },
        {
            "title": "BETIS Fasilkom UI",
            "description": (
                "Mentored 13 prospective university students through their "
                "UTBK preparation. Provided academic guidance and fostered "
                "a positive learning environment to help students stay "
                "motivated and confident throughout their preparation."
            ),
            "category": "committee",
            "started_at": datetime(2026, 2, 1),
            "ended_at": datetime(2026, 6, 30),
        },
        {
            "title": "MOONZHER Olympiad Science Club",
            "description": (
                "Managed and recorded member attendance using Google Forms "
                "and Sheets. Monitored and evaluated student performance "
                "and scores. Taught essential economics materials and "
                "provided exercises, pre-tests, and post-tests."
            ),
            "category": "organization",
            "started_at": datetime(2023, 10, 1),
            "ended_at": datetime(2024, 12, 31),
        },
    ]

    for data in experiences:
        experience = Experience.objects.create(
            title=data["title"],
            description=data["description"],
            category=data["category"],
            ended_at=data["ended_at"],
        )

        Experience.objects.filter(pk=experience.pk).update(
            started_at=data["started_at"]
        )


def reverse_seed_experience_data(apps, schema_editor):
    Experience = apps.get_model("main", "Experience")

    titles = [
        "PT Vinix Seven Aurum",
        "SIWAK-NG 2026",
        "Indonesia Technology & Innovation (INTI) Asia Expo 2026",
        "COMPFEST 18",
        "FUKI Fasilkom UI",
        "Dasar-Dasar Pemrograman 0",
        "BETIS Fasilkom UI",
        "MOONZHER Olympiad Science Club",
    ]

    Experience.objects.filter(title__in=titles).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_alter_experience_category"),
    ]

    operations = [
        migrations.RunPython(
            seed_experience_data,
            reverse_seed_experience_data,
        ),
    ]