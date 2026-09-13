from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="experience",
            name="category",
            field=models.CharField(
                max_length=20,
                choices=[
                    ("internship", "Internship"),
                    ("volunteer", "Volunteer"),
                    ("committee", "Committee"),
                    ("organization", "Organization"),
                ],
                default="internship",
            ),
        ),
    ]