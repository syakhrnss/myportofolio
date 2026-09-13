from django.db import migrations


def seed_projects(apps, schema_editor):
    Project = apps.get_model("main", "Project")

    Project.objects.bulk_create([
        Project(
            title="Smart Road Crack Inspection System",
            subtitle="AI & Deep Learning Bootcamp — FRG Universitas Brawijaya · 2026",
            image="img/project1.png",
            description=(
                "AI-powered road crack inspection system using a "
                "MobileNetV2-based U-Net architecture to perform semantic "
                "segmentation and identify crack regions from road images. "
                "The system analyzes detected cracks through metrics such as "
                "area, length, density, and severity."
            ),
        ),

        Project(
            title="Marketplace Customer Review Sentiment Analysis",
            subtitle="Data Science Intern — PT Vinix Seven Aurum · 2026",
            image="img/project2.png",
            description=(
                "Developed a machine learning application to classify "
                "Tokopedia customer reviews into positive, negative, or "
                "neutral sentiments using TF-IDF and Multinomial Naive Bayes, "
                "with an interactive Streamlit interface for sentiment prediction."
            ),
        ),

        Project(
            title="Kitchenware Sales Dashboard",
            subtitle="Karirnex Data Analyst Bootcamp · 2026",
            image="img/project3.png",
            description=(
                "Developed an interactive sales dashboard to analyze business "
                "performance, sales trends, product performance, and order "
                "completion metrics, transforming sales data into actionable "
                "insights for data-driven decision-making."
            ),
        ),

        Project(
            title="Personal Portfolio Website",
            subtitle="Personal Project · 2026",
            image="img/project4.png",
            description=(
                "Designed and developed a personal portfolio website using "
                "HTML, CSS, and Django to showcase my projects, experiences, "
                "and skills. Implemented a structured layout with reusable "
                "Django templates and responsive styling."
            ),
        ),

        Project(
            title="Grant Thornton China Market Research",
            subtitle="Business Development RIT Internship · 2026",
            image="img/project5.png",
            description=(
                "Conducted secondary research to identify and shortlist "
                "potential partners, corporations, and law firms for Grant "
                "Thornton’s services in China. Developed a stakeholder "
                "relationship map, power/interest grid, and use case analysis "
                "while collaborating with a global peer team."
            ),
        ),
    ])


def remove_projects(apps, schema_editor):
    Project = apps.get_model("main", "Project")
    Project.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_project_alter_experience_role"),
    ]

    operations = [
        migrations.RunPython(seed_projects, remove_projects),
    ]

