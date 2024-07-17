from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_ROLE_CHOICES = (
        ('user', 'user'),
        ('manager', 'manager'),
        ('admin', 'admin')
    )

    user_role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateField()
    durability = models.CharField(max_length=20, verbose_name='kurs davomiyligi')

    class Meta:
        unique_together = ['title']

    def __str__(self):
        return self.title


class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Video(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    uploaded = models.DateField()
    file = models.FileField(upload_to='videos', validators=[
        FileExtensionValidator(allowed_extensions=['mp4', 'mov', 'avi', 'wmv'])
    ])

    def __str__(self):
        return self.file.name


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text


class LikeDislike(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name='likes')
    like = models.BooleanField(verbose_name='like or dislike')

    class Meta:
        unique_together = ['author', 'course']

    def __str__(self):
        if self.like:
            return 'Like'
        return 'Dislike'


class Message(models.Model):
    title = models.CharField(max_length=100, default='Online Kurs Platformasi')
    text = models.TextField()

    def __str__(self):
        return self.title
