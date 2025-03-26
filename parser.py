import shutil
import re
from bs4 import BeautifulSoup
import requests
import aiohttp
import asyncio
import os


async def fetch(s: aiohttp.ClientSession, url: str):
    async with s.get(url) as r:
        return await r.read()


async def fetch_all(s: aiohttp.ClientSession, img_urls: list):
    tasks = []
    for url in img_urls:
        task = asyncio.create_task(fetch(s, url))
        tasks.append(task)
    res = await asyncio.gather(*tasks)
    return res


def fetch_img_links(url: str) -> list:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')

    # Формирование списка со всеми ссылками на изображения
    image_links = []
    domain = re.search(r'https?://[^/]+', url).group()  # Может ошибка вылететь, если сайт не http(s)
    http = re.search(r'https?:', url).group()
    for item in soup.find_all('img'):
        # Поиск ссылки в img
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

    return image_links


def check_website_access(url: str) -> str:
    try:
        page = requests.get(url)
        if page.status_code in range(200, 300):
            return 'done'
    except Exception as e:
        return f'Не удалось получить доступ к сайту: {e}'


async def parser(url: str) -> None:
    # Проверка доступа к сайту
    status = check_website_access(url)
    if status != 'done':
        print(status)
        return

    # Массив из ссылок на изображения
    image_links = fetch_img_links(url)

    if len(image_links) == 0:
        print("Не найдены изображения на сайте! Подходящий формат png, jpeg, jpg")
        return

    # Асинхронное получение двоичных изображений
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            imgs = await fetch_all(session, image_links)
    except Exception as e:
        print(f"Не удалось получить изображение. Попробуйте снова. {e}")
        return

    # Путь images/parsed_images/название_изображения
    path_parsed_images = 'images/parsed_images'
    path = os.path.join(path_parsed_images, url.split("/")[-1])

    # Очищаем папку parsed_images
    if os.path.exists(path_parsed_images):
        shutil.rmtree(path_parsed_images)

    # Скачка файлов по нужным папкам
    for img, img_url in zip(imgs, image_links):

        # Создаем папку с именем файла
        filename = img_url.split('/')[-1]  # Имя файла с расширением
        file_folder = os.path.join(path, filename)
        if os.path.exists(file_folder):  # Если попался файл с существующим названием
            c = 2
            while os.path.exists(file_folder + f' ({c})'):
                c += 1
            file_folder += f' ({c})'

        os.makedirs(file_folder, exist_ok=True)  # Создаем папку с именем файла

        try:  # Загружаем изображения
            file_extension = filename.split('.')[-1]
            if img is None:
                raise IOError("Не удалось скачать файл")
            with open(os.path.join(file_folder, f'default.{file_extension}'), 'wb') as f:
                f.write(img)

            print(f'Скачано: {img_url}')

        except Exception as e:
            print(f'Не удалось скачать файл {img_url}')
            shutil.rmtree(file_folder)  # Удаляем созданную папку для этого файла

def main():
    address = input("Введите адрес: ").strip()
    asyncio.run(parser(address))

main()
