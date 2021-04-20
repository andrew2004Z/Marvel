from django.contrib import admin
from .models import Comics, Users
from .forms import ComicsForm, UsersForm


# Register your models here.

@admin.register(Comics)
class ComicsAdmin(admin.ModelAdmin):
    list_display = ('name', 'file_id', 'cover_id', 'colpage_pdf', 'count_views')
    form = ComicsForm


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'type_user', 'count_reads')
    form = UsersForm
