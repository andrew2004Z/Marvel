from django.contrib import admin
from .models import Comics, Users, PopularComics
from .forms import ComicsForm, UsersForm, PopularComicsForm


# Register your models here.

@admin.register(Comics)
class ComicsAdmin(admin.ModelAdmin):
    list_display = ('name', 'file_id', 'cover_id', 'colpage_pdf', 'count_views')
    list_filter = ('count_views',)
    form = ComicsForm


@admin.register(PopularComics)
class PopularComicsAdmin(admin.ModelAdmin):
    list_display = ('name', 'file_id', 'cover_id', 'colpage_pdf', 'count_views')
    list_filter = ('count_views',)
    form = PopularComicsForm


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'type_user', 'username', 'password')
    form = UsersForm
