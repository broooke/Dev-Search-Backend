from projects.models import Project, Review, Tag
from django.contrib import admin

# Register your models here.

admin.site.register(Project)
admin.site.register(Tag)
admin.site.register(Review)