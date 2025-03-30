import telebot
from telebot import types
import os
from parser import scrape_and_save_images
from image_formatter import ImageFormatter
from config import TOKEN, PHOTOS_PATH
bot = telebot.TeleBot(TOKEN, skip_pending=True)
formatter = ImageFormatter()

def user_menu():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Выбрать изображение','Поменять ссылку')
    return markup

def select(name):
    for i in os.listdir(path):
        if i.startswith(name):
            send_photo = path + "/" + i
            send_photo = types.InputMediaPhoto(open(send_photo, 'rb'))
            return(send_photo)
    return

def PTL_menu():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Повернуть изображение', 'Отзеркалить','Обрезать',\
               'Изменить размер', 'Сделать чёрно-белым', 'Преобразовать в цветовой диапазон',\
                'Размытие', 'Увеличьте резкость', 'Сглаживание', 'Найти рёбра',\
                'Яркость',  'Добавить текст', 'Главное меню')
    return markup

def get_photos():
    photos = []
    paths = []
    for photo_folder in os.listdir(PHOTOS_PATH):
        try:
            int(photo_folder[:3])
            for photo in os.listdir(PHOTOS_PATH + "/" + photo_folder):
                if photo.startswith("default"):
                    paths.append(PHOTOS_PATH + "/" + photo_folder)
                    photo = PHOTOS_PATH + "/" + photo_folder + "/" + photo
                    photos.append(types.InputMediaPhoto(open(photo, 'rb')))
                    
        except Exception as e:
            print(e)
    return photos, paths

def send_res(message, name):
    send_photo = select(name)
    bot.send_media_group(message.chat.id, [send_photo])
    bot.send_message(message.chat.id, 'Выберете действие', reply_markup=PTL_menu())
@bot.message_handler(commands=['start'])
def bot_start(message):
    bot.send_message(message.chat.id, 'Приветствую! \n Я бот для обработки спаршеных изображений, дабы воспользоваться моими функциями введите url')

@bot.message_handler(func=lambda message: message.text.startswith('Главное меню'))
def bot_main_menu(message):
    bot.send_message(message.chat.id, 'Выберете действие', reply_markup=user_menu())
    
@bot.message_handler(func=lambda message: message.text.startswith('http'))
def bot_parce(message):
    scrape_and_save_images(message.text)
    photos, paths = get_photos()
    
    bot.send_media_group(message.chat.id, photos)
    
    bot.send_message(message.chat.id, 'Изображения спаршены', reply_markup=user_menu())

@bot.message_handler(func=lambda message: message.text == 'Выбрать изображение')
def bot_select_image(message):
    photos, paths = get_photos()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for i in range(1, len(photos) + 1):
        markup.add(str(i))
    markup.add("Главное меню")
    bot.send_message(message.chat.id, 'Выберете номер изобржения', reply_markup=markup)
    bot.register_next_step_handler(message, bot_selected_image, photos, paths)

def bot_selected_image(message, photos, paths):
    try:
        index = int(message.text) -1
        global path
        path = paths[index]
        formatter.select_image_directory(path)
        bot.send_media_group(message.chat.id, [photos[index]])
        bot.send_message(message.chat.id, 'Выберете действие', reply_markup=PTL_menu())
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Возможно изображения с таким индексом нет', reply_markup=PTL_menu())

@bot.message_handler(regexp="Повернуть изображение")
def rotate_image(message):
    bot.reply_to(message, "Выберете градус поворота")
    bot.register_next_step_handler(message, rotated_image)
def rotated_image(message):
    try:
        rotate = int(message.text)
        formatter.rotate_image(rotate)
        send_res(message, "rotated")
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Ошибка ввода', reply_markup=PTL_menu())

    
@bot.message_handler(regexp="Отзеркалить")
def flip_image(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add('По горизонтали', 'По вертикали')
    bot.send_message(message.chat.id, "Выберете градус поворота", reply_markup=markup )
    bot.register_next_step_handler(message, fliped_image)
def fliped_image(message):
    if message.text == 'По горизонтали':
        mode = "horizontal"
    elif message.text == 'По вертикали':
        mode = "vertical"
    else:
        bot.send_message(message.chat.id, 'Такого отзеркаливания у нас нету', reply_markup=PTL_menu())
    formatter.flip_image(mode)
    send_res(message, "flipped")

@bot.message_handler(regexp="Обрезать")
def crop_image(message):
    # Логика обрезки изображения
    bot.send_message(message.chat.id, 'Возвращайся позже', reply_markup=PTL_menu())

@bot.message_handler(regexp="Изменить размер")
def resize_image(message):
    # Логика изменения размера изображения
    bot.reply_to(message, "Введите % изменения ширины и высоты")
    bot.register_next_step_handler(message, resized_image)
def resized_image(message):
    try:
        message_text = message.text.split(" ")
        formatter.resize_image(int(message_text[0]), int(message_text[1]))
        send_photo = select('resized')
        bot.send_media_group(message.chat.id, [send_photo])
        bot.send_message(message.chat.id, 'Выберете действие', reply_markup=PTL_menu())
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Ошибка ввода', reply_markup=PTL_menu())
@bot.message_handler(regexp="Сделать чёрно-белым")
def grayscale_image(message):
    formatter.grayscale_image()
    send_res(message, 'grayscaled')
    
@bot.message_handler(regexp="Преобразовать в цветовой диапазон")
def color_range_image(message):
    # Логика преобразования изображения в цветовой диапазон
    markup = types.ReplyKeyboardMarkup()
    markup.add("Красный", "Зелёный", "Голубой")
    bot.send_message(message.chat.id, 'Выберете цвет', reply_markup=markup)
    bot.register_next_step_handler(message, color_ranged_image)
def color_ranged_image(message):
    if message.text =="Красный":
        color = "r"
    elif message.text == "Зелёный":
        color = "g"
    elif message.text == "Голубой":
        color = "b"
    else:
        bot.send_message(message.chat.id, 'Что-то не то', reply_markup=PTL_menu())
        return
    formatter.chanel_convert_image(color)
    send_res(message, 'chanel_converted')

@bot.message_handler(regexp="Размытие")
def blur_image(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add("Прямоугольное", "Гауссово")
    bot.send_message(message.chat.id, 'Выберете тип размытия', reply_markup=markup)
    bot.register_next_step_handler(message, blur_image_val)
def blur_image_val(message):
    if message.text == "Прямоугольное":
        mode = 'box'
    elif message.text == "Гауссово":
        mode = 'gaussian'
    else:
        bot.send_message(message.chat.id, 'Что-то не то', reply_markup=PTL_menu())
        return
    bot.send_message(message.chat.id, 'Впишите радиус размытия')
    bot.register_next_step_handler(message, blured_image_val, mode)
def blured_image_val(message, mode):
    try:
        val = int(message.text)
        formatter.blur_image(mode, val)
        send_res(message, 'blurred')
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Что-то не то', reply_markup=PTL_menu())


@bot.message_handler(regexp="Увеличьте резкость")
def sharpen_image(message):
    formatter.sharpen_image()
    send_res(message, 'sharpened')

@bot.message_handler(regexp="Сглаживание")
def smooth_image(message):
    formatter.smooth_image()
    send_res(message, 'smoothed')

@bot.message_handler(regexp="Найти рёбра")
def edge_detection(message):
    formatter.find_edges()
    send_res(message, 'edges')

@bot.message_handler(regexp="Яркость")
def brightness_adjustment(message):
    # Логика регулировки яркости изображения
    bot.send_message(message.chat.id, 'Введите число, все что выше 1.0 увеличивает яркость, и наоборот')
    bot.register_next_step_handler(message, brightnessed_adjustment)
def brightnessed_adjustment(message):
    try:
        val = float(message.text)
        formatter.change_brightness(val)
        send_res(message, 'brightness_changed')
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Что-то не то', reply_markup=PTL_menu())


@bot.message_handler(regexp="Добавить текст")
def add_text(message):
    try:
        bot.send_message(message.chat.id, 'Введите текст который хотите добваить на изображение')
        bot.register_next_step_handler(message, add_text_place)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Ошибка ввода', reply_markup=PTL_menu())
def add_text_place(message):
    try:
        text = message.text
        total = [text]
        bot.send_message(message.chat.id, 'Введите x и y текста, через пробел')
        bot.register_next_step_handler(message, add_text_font, total)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Ошибка ввода', reply_markup=PTL_menu())
def add_text_font(message, total):
    try:
        message_val = message.text.split(" ")
        x = int(message_val[0])
        y = int(message_val[1])
        total.append(x)
        total.append(y)
        bot.send_message(message.chat.id, 'Шрифт ')
        bot.register_next_step_handler(message, add_text_color, total)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Ошибка ввода', reply_markup=PTL_menu())
def add_text_color(message, total):
    try:
        total.append(int(message.text))
        bot.send_message(message.chat.id, 'Введите r g b параметры')
        bot.register_next_step_handler(message, added_text_color, total)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Ошибка ввода', reply_markup=PTL_menu())
def added_text_color(message, total):
    try:
        color = tuple(map(int, message.text.split(" ")))
        formatter.add_text(*total, color)
        send_res(message, 'text_added')
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Ошибка ввода', reply_markup=PTL_menu())

if __name__ == "__main__":
    bot.polling(non_stop=True)