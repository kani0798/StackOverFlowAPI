from django.contrib import admin

# Register your models here.
from .models import CodeImage, Problema, Reply, Comment


class ImageInline(admin.TabularInline):
    model = CodeImage
    min_num = 1
    max_num = 5


@admin.register(Problema)
class ProblemAdmin(admin.ModelAdmin):
    inlines = [ImageInline]


admin.site.register(Reply)
admin.site.register(Comment)
