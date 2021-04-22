from aparser.models import Comics
import pandas as pd
import telebot

bot = telebot.Telebot('')

def get_info_comics():
    try:
        retro = Comics.objects.filter()
        return retro.values().get()
    except Comics.DoesNotExist:
        return False

def popular():
    data_comics = get_info_comics()
    df = pd.DataFrame(data_comics)
    data_popular = df.sort_values('count_views')[:5]
    sp_data = []
    for i in data_popular:
        file_info = bot.get_file(i['cover_id'])
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'files/' + i['name']
        sp_data.append([i['name'], src, i['count_views']])
        new_file = open(src, 'wb')
        new_file.write(downloaded_file)
        new_file.close()
    return sp_data

