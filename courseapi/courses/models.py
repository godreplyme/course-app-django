from tkinter.constants import CASCADE

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Model, PROTECT, CharField, ForeignKey
from ckeditor.fields import RichTextField


# Create your models here.
class User(AbstractUser):
    pass

class BaseModel(Model):
    active = models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['-id']
    def __str__(self):
        return self.name


class Course(BaseModel):
    subject = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='static/%Y/%m', null=True, blank=True)
    category =models.ForeignKey(Category,on_delete=models.PROTECT)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.subject

class Lesson(BaseModel):
    name = CharField(max_length=100, unique=True)
    content = RichTextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name