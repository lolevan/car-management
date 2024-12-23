from django.contrib import admin
from .models import Car, Comment


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'owner', 'created_at', 'updated_at')
    search_fields = ('make', 'model', 'owner__username')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('car', 'author', 'created_at')
    search_fields = ('car__make', 'car__model', 'author__username')
