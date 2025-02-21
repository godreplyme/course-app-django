from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.urls import path

from .models import Course, Category, Lesson
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'description']
    readonly_fields = ['avatar']
    def avatar(self, obj):
        if obj:
            return mark_safe('<img src="/static/{url}" width="120px" />'.format(url=obj.image.name))

class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Lesson
        fields = '__all__'

class LessonAmin(admin.ModelAdmin):
    form = LessonForm

class CourseAppAdminSite(admin.AdminSite):
    site_header = 'Hệ thống khoá học trực tuyến'

    def get_urls(self):
        return [path('course-stats/', self.stats_view)] + super().get_urls()

    def stats_view(self, request):
        count = Course.objects.filter(active=True).count()

        stats = Course.objects.annotate(lesson_count=Count('my_lesson')).values('id', 'subject', 'lesson_count')
        return TemplateResponse(request,'admin/course-stats.html', {'course_count': count,'course_stats': stats})

admin_site = CourseAppAdminSite(name='myadmin')

admin.site.register(Category)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAmin)
# Register your models here.
