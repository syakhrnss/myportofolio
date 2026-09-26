import uuid

from django.contrib.auth.models import User
from django.db import models 


class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('volunteer', 'Volunteer'),
        ('committee', 'Committee'),
        ('organization', 'Organization'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='internship')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateField()
    ended_at = models.DateField(blank=True, null=True)
    role = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None

class Project(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    image = models.URLField(max_length=500, blank=True)
    description = models.TextField()
    starred_by = models.ManyToManyField(
        User, related_name="starred_projects", blank=True
    )

    def __str__(self):
        return self.title