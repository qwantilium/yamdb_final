from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title, User


@admin.register(User, Category, Genre, GenreTitle, Title, Review, Comment)
class ProjectModelsAdmin(admin.ModelAdmin):

    list_display = ('id', '__str__',)

    empty_value_display = "-пусто-"
