# -*- coding: utf-8 -*-
from django.contrib import admin
from ineo.models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'cdate', 'status']
    search_fields = ['title', 'email', 'comment']
    list_filter = ['status', 'content_type']
    list_per_page = 25
admin.site.register(Comment, CommentAdmin)
