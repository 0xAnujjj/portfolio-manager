from django.db import models

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    github_link = models.URLField(blank=True)
    live_link = models.URLField(blank=True)
    tech_stack = models.CharField(max_length=200, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title