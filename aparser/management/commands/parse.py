import requests
import os
from fake_useragent import UserAgent
import time
import glob
import img2pdf
import PyPDF2
from bs4 import BeautifulSoup
import json
from django.core.management.base import BaseCommand
from aparser.models import Comics
import telebot


def colpage_pdf(path):
    pdf_file = open(path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    num_pages = pdf_reader.numPages
    return num_pages


def img_to_pdf_one(path1, path2):
    try:
        path = path1 + '/' + path2
        if not os.path.exists(f'{path}/{path2}.pdf'):
            with open(f'{path}/{path2}.pdf', "wb") as f:
                f.write(img2pdf.convert(glob.glob(path + "\*.jpg")))
    except Exception as e:
        print(e)


def generate_headers():
    ua = UserAgent()
    return {'user-agent': ua.random}


class ComicsParser:
    def __init__(self, json_path, token):
        self.json_path = json_path
        self.bot = telebot.TeleBot(token)

    def get_comics_uni(self, path, url, col_null, g):
        try:
            i = g
            if col_null == 2:
                p = requests.get(f'{url}/00{i}.jpg',
                                 headers=generate_headers())
            else:
                p = requests.get(f'{url}/0{i}.jpg', headers=generate_headers())
            if p.status_code == 200:
                try:
                    os.mkdir(path)
                except:
                    pass
                if g == 0:
                    out = open(f"{path}/00{i + 1}.jpg", "wb")
                else:
                    out = open(f"{path}/00{i}.jpg", "wb")
                out.write(p.content)
                out.close()
                i += 1
                while p.status_code == 200:
                    if i < 10:
                        if col_null == 2:
                            p = requests.get(f'{url}/00{i}.jpg',
                                             headers=generate_headers())
                        else:
                            p = requests.get(f'{url}/0{i}.jpg',
                                             headers=generate_headers())
                        if p.status_code == 404:
                            break
                        if g == 0 and i == 9:
                            out = open(f"{path}/0{i + 1}.jpg", "wb")
                        elif g == 0:
                            out = open(f"{path}/00{i + 1}.jpg", "wb")
                        else:
                            out = open(f"{path}/00{i}.jpg", "wb")
                        out.write(p.content)
                        out.close()
                    elif i < 100:
                        if col_null == 2:
                            p = requests.get(f'{url}/0{i}.jpg',
                                             headers=generate_headers())
                        else:
                            p = requests.get(f'{url}/{i}.jpg',
                                             headers=generate_headers())
                        if p.status_code == 404:
                            break
                        if g == 0:
                            out = open(f"{path}/0{i + 1}.jpg", "wb")
                        else:
                            out = open(f"{path}/0{i}.jpg", "wb")
                        out.write(p.content)
                        out.close()
                    else:
                        if col_null == 2:
                            p = requests.get(f'{url}/{i}.jpg',
                                             headers=generate_headers())
                        else:
                            p = requests.get(f'{url}/{i}.jpg',
                                             headers=generate_headers())
                        if p.status_code == 404:
                            break
                        if g == 0:
                            out = open(f"{path}/{i + 1}.jpg", "wb")
                        else:
                            out = open(f"{path}/{i}.jpg", "wb")
                        out.write(p.content)
                        out.close()
                    i += 1
        except ConnectionError:
            print('ConnectionError')
            time.sleep(10)
            ComicsParser.get_comics_uni(self, path, url, col_null, g=g)
        except Exception as e:
            print(e)
            time.sleep(10)
            ComicsParser.get_comics_uni(self, path, url, col_null, g=g)

    def get_comics_one(self, chat_id, db_comics, path1, path2):
        try:
            name = f'{path2}'
            cover = self.bot.send_photo(
                chat_id, open(f'{path1}\{name}\\001.jpg', 'rb'))
            msg = self.bot.send_document(chat_id, open(
                f'{path1}\{name}\{name}.pdf', 'rb'))
            comics_id = msg.document.file_id
            cover_id = cover.photo[0].file_id
            time.sleep(1)
            return (name, comics_id, cover_id, colpage_pdf(f'{path1}\{name}\{name}.pdf'))
        except Exception as e:
            print(e)

    def run_get_comics_uni(self, path11, url, sp_num):
        for x in range(sp_num[0], sp_num[1]):
            path1 = path11 + str(x)
            sp = path1.split('/')
            if x < 10:
                url1 = url + f'00{x}'
            elif x < 100:
                url1 = url + f'0{x}'
            else:
                url1 = url + f'{x}'
            if not os.path.exists(path1 + '/' + path1.split('/')[-1] + '.pdf'):
                print(path1 + '/' + path1.split('/')[-1] + '.pdf')
                ComicsParser.get_comics_uni(
                    self, path=path1, url=url1, col_null=2, g=0)
                img_to_pdf_one(
                    '/'.join(path1.split('/')[:-1]), path1.split('/')[-1])
                try:
                    try:
                        p = Comics.objects.get(name=path1.split('/')[-1])
                        print('in base')
                    except Comics.DoesNotExist:
                        sp = list(ComicsParser.get_comics_one(
                            self, '604900292', 'db_comics', '/'.join(path1.split('/')[:-1]), path1.split('/')[-1]))
                        p = Comics(
                            name=sp[0],
                            file_id=sp[1],
                            cover_id=sp[2],
                            colpage_pdf=sp[3],
                            count_views=0
                        ).save()
                        print(p)
                except Exception as e:
                    print(e)
                    pass
            else:
                print('File found: ' + path1)
                try:
                    try:
                        p = Comics.objects.get(name=path1.split('/')[-1])
                        print('in base')
                    except Comics.DoesNotExist:
                        sp = list(ComicsParser.get_comics_one(
                            self, '604900292', 'db_comics', '/'.join(path1.split('/')[:-1]), path1.split('/')[-1]))
                        p = Comics(
                            name=sp[0],
                            file_id=sp[1],
                            cover_id=sp[2],
                            colpage_pdf=sp[3],
                            count_views=0
                        ).save()
                        print(p)
                except Exception as e:
                    print(e)
                    pass

    def run_get_comics_one(self, path11, url, sp_num):
        for x in range(sp_num[0], sp_num[1]):
            path1 = path11 + str(x)
            if x < 10:
                url1 = url + f'00{x}'
            elif x < 100:
                url1 = url + f'0{x}'
            else:
                url1 = url + f'{x}'
            ComicsParser.get_comics_uni(self, path=path1, url=url1, col_null=2, g=0)

    def get_name_comics(self, url):
        sp1 = []
        sp = []
        sp2 = []
        sp3 = []
        p = requests.get(url, headers=generate_headers()).content
        soup = BeautifulSoup(p, 'lxml')
        ui = soup.find_all('h4', class_='field-content')
        for i in ui:
            sp.append([i.text, 'https://drawnstories.ru/' + i.find('a')['href']])
        for i in sp:
            p1 = requests.get(i[1], headers=generate_headers()).content
            soup1 = BeautifulSoup(p1, 'lxml')
            ui1 = soup1.find_all('h4', class_='field-content')
            for i in ui1:
                sp1.append(
                    [i.text, 'https://drawnstories.ru/' + i.find('a')['href']])
        for i in sp1:
            p2 = requests.get(i[1], headers=generate_headers()).content
            soup2 = BeautifulSoup(p2, 'lxml')
            soup3 = BeautifulSoup(p2, 'lxml')
            h1 = soup2.find('h1', class_='page-header').text
            try:
                sp_v = soup3.find_all(
                    'div', class_='field-item even')[1].find_all('div')
            except IndexError as e:
                pass
            for i in sp_v:
                try:
                    url11 = i.find('a')['href']
                    if 'http' in url11 and 'vk.com' not in url11:
                        sp_path = url11[:-11][:-1].split('/')[-1].split('-')
                        path = []
                        for i in sp_path:
                            path.append(i.capitalize())
                        if url11[:-11][-1] == '-':
                            sp3.append(['1 - RU/' + ' '.join(path) +
                                        ' '.join(path) + ' #', url11[:-11]])
                            break
                except Exception as e:
                    pass
        for i in sp3:
            try:
                os.mkdir(i[0].split('/')[-2])
            except:
                pass
            ComicsParser.run_get_comics_uni(self, i[0], i[1], [1, 1000])

    def parse_add_json(self, url):
        p = requests.get(url)
        if p.status_code == 200:
            soup = BeautifulSoup(p.content, 'lxml')
            dict1 = {}
            dict1[soup.find('h1', class_='page-header').text] = {}
            for i in soup.find_all('div', 'views-field views-field-name'):
                try:
                    p1 = requests.get(
                        'https://drawnstories.ru/' + i.find('a')['href'])
                    if p.status_code == 200:
                        soup1 = BeautifulSoup(p1.content, 'lxml')
                        try:
                            dict1[soup.find('h1', class_='page-header').text][soup1.find('h1').text.split(
                                ' / ')[-1]] = soup1.find('div', class_='big1').find('img')['src'][:-5]
                        except:
                            dict1[soup.find('h1', class_='page-header').text][soup1.find('h1').text.split(
                                ' / ')[-1]] = soup1.find('div', class_='ds11').find('img')['src'][:-5]
                    else:
                        print('ERORR')
                except Exception as e:
                    print(e)
            with open("data_file.json", "a", encoding='utf-8') as write_file:
                json.dump(dict1, write_file, ensure_ascii=False)
        else:
            print('ERORR 404')

    def read_json(self, path):
        with open(path, "r", encoding='utf-8') as read_file:
            data = json.load(read_file)
            return data

    def parse_json(self, json_parse):
        for i in json_parse['url_comics']['Marvel'].keys():
            try:
                os.mkdir('Comics/' + i)
            except:
                pass
            for j in json_parse['url_comics']['Marvel'][i].keys():
                try:
                    os.mkdir('Comics/' + i + '/' + j.replace(':', " -"))
                except:
                    pass
                ComicsParser.run_get_comics_uni(self,
                                                'Comics/' + i + '/' + j.replace(
                                                    ':', " -") + '/' + j.replace(':', " -") + ' #',
                                                json_parse['url_comics']['Marvel'][i][j], [0, 200])

    def main(self):
        ComicsParser.parse_json(
            self, ComicsParser.read_json(self, self.json_path))


class Command(BaseCommand):
    help = 'Парсинг DrawnStoRies'

    def handle(self, *args, **options):
        p = ComicsParser('data_json/comics.json',
                         '1417817254:AAGRJdZkQSsNgWZO7Sfp8REFD1aepTPSGJg')
        p.main()
