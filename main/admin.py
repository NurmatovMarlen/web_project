from django.contrib import admin

from .models import *

class ImageInLineAdmin(admin.TabularInline):
    model=Image
    fields=('image',)
    max_num=3

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = [ImageInLineAdmin,]

admin.site.register(Category)


