from django.contrib import admin
from .models import *


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'create_time', 'update_time', 'category', 'author']

admin.site.register(Article,ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)
# Register your models here.
