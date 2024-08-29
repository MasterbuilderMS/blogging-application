from django.contrib import admin
from . import models


class CommentInline(admin.TabularInline):
    model = models.Comment
    extra = 3


class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'post', 'date_posted', 'active')
    list_filter = ('active', 'date_posted')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment, CommentAdmin)
