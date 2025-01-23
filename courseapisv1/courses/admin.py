from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from courses.models import Category, Course, Lesson, Tag, Comment
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path


class MyCourseAdmin(admin.AdminSite):
    site_header = 'HỆ THỐNG OU eCourse'

    def get_urls(self):
        return [path('stats/', self.stats)] + super().get_urls()

    def stats(self, request):
        stats = Category.objects.annotate(count=Count('course__id')).values('id', 'name', 'count')
        return TemplateResponse(request, 'admin/stats.html', {
            'stats': stats
        })


class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Lesson
        fields = '__all__'


class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'active', 'created_date']
    search_fields = ['subject', 'content']
    list_filter = ['id', 'subject', 'created_date']
    list_editable = ['subject']
    readonly_fields = ['avatar']
    form = LessonForm

    def avatar(self, lesson):
        return mark_safe(f"<img src='/static/{lesson.image.name}' width='200' />")

    class Media:
        css = {
            'all': ('/static/css/style.css', )
        }


admin_site = MyCourseAdmin()

admin_site.register(Category)
admin_site.register(Course)
admin_site.register(Lesson, LessonAdmin)
admin_site.register(Tag)
admin_site.register(Comment)
