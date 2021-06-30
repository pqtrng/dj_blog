from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)  # post title
    slug = models.SlugField(
        max_length=250, unique_for_date='publish')  # for URL
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()  # body of the post
    publish = models.DateTimeField(default=timezone.now)  # time of publishing
    created = models.DateTimeField(auto_now_add=True)  # time of creation
    updated = models.DateTimeField(auto_now=True)  # time of update
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        # sort results by publish field in descending order (-) when query database
        ordering = ('-publish',)

    def __str__(self):
        return self.title  # for better representation in adminitration site
