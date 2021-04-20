from django.db import models

from django.db import models


class Comics(models.Model):
    name = models.TextField(
        verbose_name='Название',
    )

    file_id = models.TextField(
        verbose_name='ID комикса',
    )

    cover_id = models.TextField(
        verbose_name='ID обложки комикса',
    )

    colpage_pdf = models.PositiveIntegerField(
        verbose_name='Количество страниц',
    )

    count_views = models.PositiveIntegerField(
        verbose_name='Количество просмотров',
    )

    class Meta:
        verbose_name = 'Comics'
        verbose_name_plural = 'Comics'


class Users(models.Model):
    user_id = models.TextField(
        verbose_name='ID пользователя',
    )

    type_user = models.TextField(
        verbose_name='Права пользователя',
    )

    count_reads = models.PositiveIntegerField(
        verbose_name='Количество прочтений',
    )

    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'
