import shutil
import re
from bs4 import BeautifulSoup
import requests
import aiohttp
import asyncio
import os


async def _fetch(s: aiohttp.ClientSession, url: str) -> str:
    async with s.get(url) as r:
        return await r.read()


# Подумать о возвращения статуса парсинга изображения
async def _fetch_all(s: aiohttp.ClientSession, img_urls: list) -> list:
    tasks = []
    for url in img_urls:
        task = asyncio.create_task(_fetch(s, url))
        tasks.append(task)
    res = await asyncio.gather(*tasks)
    return res


def _fetch_img_links(url: str) -> list:
    page = requests.get(url)  # Тут может все сломаться
    soup = BeautifulSoup(page.text, 'lxml')
    # Формирование списка со всеми ссылками на изображения
    image_links = []

    # Определение корневой ссылки (domain)
    domain = re.search(r'https?://[^/]+', url).group()
    http = re.search(r'https?:', url).group()
    for item in soup.find_all('img'):
        # Поиск ссылки на изображение в img
        link = item.get('data-src') or item.get('src')
        if not link:
            # Ссылка не найдена
            continue

        # Если изображение не того формата, то не добавляем
        if re.search(r'[.](png|jpg|jpeg)$', link) is None:
            continue

        if link.startswith('http'):
            image_links.append(link)
        elif link.startswith('//'):
            image_links.append(http + link)
        elif link.startswith('/'):
            image_links.append(domain + link)
        else:
            image_links.append(domain + '/' + link)

    return image_links


def _check_website_access(url: str) -> str:
    try:
        page = requests.get(url)
        if page.status_code in range(200, 300):
            return 'done'
        return f'Failed to access the site: status_code {page.status_code}'
    except Exception as e:
        return f'Failed to access the site: {e}'


async def _parser(url: str) -> tuple:
    # Сохраняю ошибки, если не удалось запарсить/скачать фото
    download_error = []

    # Очистка ссылки от лишних пробелов и добавляем http://
    url = url.strip()
    if not url.startswith('http'):
        url = 'http://' + url

    # Проверка доступа к сайту
    status = _check_website_access(url)
    if status != 'done':
        return 'error', status

    # Массив из ссылок на изображения
    image_links = _fetch_img_links(url)
    if len(image_links) == 0:
        return 'error', 'No images found on the site! Suitable format png, jpeg, jpg'

    # Асинхронное получение изображений в двоичном представление
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            imgs = await _fetch_all(session, image_links)
    except Exception as e:
        return 'error', f'Failed to retrieve the image. Try again. {e}'

    # Путь images/parsed_images/название_изображения
    path_parsed_images = 'images/parsed_images'

    # Очищаем папку parsed_images
    if os.path.exists(path_parsed_images):
        shutil.rmtree(path_parsed_images)

    # Скачка файлов по нужным папкам
    for img, img_url in zip(imgs, image_links):

        # Создаем папку с именем файла
        filename = img_url.split('/')[-1]  # Имя файла с расширением
        file_folder = os.path.join(path_parsed_images, filename)
        if os.path.exists(file_folder):  # Если попался файл с существующим названием
            c = 2
            while os.path.exists(file_folder + f' ({c})'):
                c += 1
            file_folder += f' ({c})'
        os.makedirs(file_folder, exist_ok=True)  # Создание папки с именем файла

        # Если не удалось запарсить изображение
        if img is None:
            download_error.append(f"Failed to download a file: {img_url}")
            shutil.rmtree(file_folder)  # Удаляем созданную папку для этого файла
            continue

        try:  # Загружаем изображения
            file_extension = filename.split('.')[-1]
            with open(os.path.join(file_folder, f'default.{file_extension}'), 'wb') as f:
                f.write(img)
        except Exception as e:
            shutil.rmtree(file_folder)  # Удаляем созданную папку для этого файла
            download_error.append(f'Error when writing a file: {img_url} {e}')

    return ('done', 'OK') if not download_error else ('warning', '\n'.join(download_error))


def scrape_and_save_images(url: str) -> tuple:
    return asyncio.run(_parser(url))


# ТГ бот пользуется только функцией scrape_and_save_images(), которая на вход ожидает url

# Результат функции кортеж (status, message)
# status = done/error/warning
# message = OK/текст ошибки/ текст предупреждения
# Пометка: done/warning - значит, что удалось запарсить и скачать изображения.
#                         В message warning - из-за чего не получилось скачать/запарсить изображение и ссылка на него

# Примеры работы с выводом результата функции на экран
if __name__ == '__main__':
    address = 'https://scrapingclub.com/exercise/list_basic/'
    print(scrape_and_save_images(address))
    # output: ('done', 'OK')

    # address = 'https://texterra.ru/blog/kak-sdelat-iz-stranitsy-404-chto-to-poleznoe-i-interesnoe-priаmery.html'
    # print(scrape_and_save_images(address))
    # # output: ('error', 'Failed to access the site: status_code 404')

    # Не нашел пример сайта результатом функции ('waring', message). Но вот, пример, что ожидается
    # output: ('warning', 'Failed to download a file: https://scrapingclub.com/exercise/list_basic_detail/96436-A/\n
    # Failed to download a file: https://scrapingclub.com/exercise/list_basic_detail/90008-E/')
