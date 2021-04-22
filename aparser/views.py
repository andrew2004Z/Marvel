import os
from io import BytesIO

from PIL import Image
from django.http import HttpResponse
from django.shortcuts import render
from aparser.models import PopularComics
import telebot

bot = telebot.TeleBot('1417817254:AAGRJdZkQSsNgWZO7Sfp8REFD1aepTPSGJg')


def index(request):
    return render(request, '../templates/base.html')


def popular_comics(request):
    sp_data = []
    for i in PopularComics.objects.all().values():
        file_info = bot.get_file(i['cover_id'])
        downloaded_file = bot.download_file(file_info.file_path)
        src = f"{i['name']}.jpg"
        sp_data.append([i['name'], src, i['count_views']])
        Image.open(BytesIO(downloaded_file)).save('static/temp/' + src)
    return render(request, '../templates/popular_comics.html')
