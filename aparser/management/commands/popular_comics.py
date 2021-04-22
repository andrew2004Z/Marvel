import schedule

from aparser.models import Comics, PopularComics
import pandas as pd
import telebot
from django.core.management.base import BaseCommand

bot = telebot.TeleBot('1417817254:AAGRJdZkQSsNgWZO7Sfp8REFD1aepTPSGJg')


def PopularComics_add(name, file_id, cover_id, colpage, count_views):
    PopularComics(
        name=name,
        file_id=file_id,
        cover_id=cover_id,
        colpage_pdf=colpage,
        count_views=count_views
    ).save()


def get_info_comics():
    try:
        sp = Comics.objects.all().values()
        sp_1 = []
        for i in sp:
            sp_1.append(i)
        return sp_1
    except Comics.DoesNotExist:
        return False


def popular():
    data_comics = get_info_comics()
    df = pd.DataFrame(data_comics)
    data_popular = df.sort_values('count_views')[-5:].to_dict('r')[::-1]
    # print(data_popular)
    PopularComics.objects.all().delete()
    for i in data_popular:
        print(i)
        PopularComics_add(i['name'], i['file_id'], i['cover_id'], i['colpage_pdf'], i['count_views'])
    return 0
    # for j, i in enumerate(data_popular):
    #    file_info = bot.get_file(i['cover_id'])
    #    downloaded_file = bot.download_file(file_info.file_path)
    #    src = 'files/' + i['name']
    #    sp_data.append([i['name'], src, i['count_views']])
    #    new_file = open(src, 'wb')
    #    new_file.write(downloaded_file)
    #    new_file.close()


class Command(BaseCommand):
    help = 'Запуск бота.'

    def handle(self, *args, **options):
        #schedule.every().hour.do(popular)
        #schedule.every(10).seconds.do(popular)
        #while True:
        #    schedule.run_pending()
        popular()
