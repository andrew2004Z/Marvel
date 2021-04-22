from django.db import models


class Comics(models.Model):
    name = models.TextField(
        verbose_name='Название',
        primary_key=True
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

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Комикс'
        verbose_name_plural = 'Комиксы'


class Users(models.Model):
    user_id = models.TextField(
        verbose_name='ID пользователя',
        unique=True,
    )

    type_user = models.TextField(
        verbose_name='Права пользователя',
    )

    count_reads = models.PositiveIntegerField(
        verbose_name='Количество прочтений',
    )

    username = models.TextField(
        verbose_name='Имя пользователя',
        default='user'
    )

    password = models.TextField(
        verbose_name='Пароль',
        default='password'
    )

    def __str__(self):
        return f'№{self.user_id} {self.username}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class PopularComics(models.Model):
    name = models.TextField(
        verbose_name='Название',
        primary_key=True
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

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Популярный комикс'
        verbose_name_plural = 'Популярные комиксы'
