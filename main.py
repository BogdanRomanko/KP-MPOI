# Импортируем нужные библиотеки работы с Telegram, Matlab
# путями файлов, файлами, регулярными выражениями и скриптами запуска симуляции и
# получения значений на разных температурах
import telebot
import matlab.engine
import os
from os import path
import shutil
import re
import runModel
import values

isValue = False

os.chdir(os.path.dirname(__file__))

# Создаём объект бота и подключаем его к заранее
# полученному токену этого бота
bot = telebot.TeleBot('1720738614:AAHrxMK2wQr1IgyszvwmQrcrO-ziaqQOVpg')

# Настраиваем основную клавиатуру для работы с ботом
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Получить график')
keyboard1.row('Получить значения при тепературе ...')
keyboard1.row('Получить параметры датчиков температуры')
keyboard1.row('Обновить значения датчиков')

# Настраиваем клавиатуру для получения графиков
keyboard2 = telebot.types.ReplyKeyboardMarkup()
keyboard2.row('Получить график выхода датчиков')
keyboard2.row('Получить график выхода АЦП')
keyboard2.row('Получить график выхода УК (устройства кодирования)')
keyboard2.row('Получить график выхода УД (устройства декодирования)')
keyboard2.row('Обратно')

# Настраиваем клавиатуру для получения значений на
# определённой температуре или на участке
keyboard3 = telebot.types.ReplyKeyboardMarkup()
keyboard3.row('Получить значение на определённой температуре')
keyboard3.row('Получить значение на отрезке температуры')
keyboard3.row('Получить все значения')
keyboard3.row('Обратно')

# Настраиваем клавиатуру получения параметров датчиков температуры
keyboard4 = telebot.types.ReplyKeyboardMarkup()
keyboard4.row('Получить параметры датчика температуры №1')
keyboard4.row('Получить параметры датчика температуры №2')
keyboard4.row('Получить параметры датчика температуры №3')
keyboard4.row('Получить параметры датчика температуры №4')
keyboard4.row('Обратно')

# Функция приветственного сообщения для пользователя
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
    "Привет, я - бот, разработанный в ходе работы над курсовым проектом по МПОИ\n" +
    "Студентом группы СКС-18 - Романко Б. А.\n" +
    "Моя задача - отображать данные со схем, полученных при построении модели устройства " + 
    "передачи данных, кодирующего - декодирующего устройства, дополнительного варианто кода для передачи команд \n" +
    "Пожалуйста, выберите действие, которое хотите чтобы я сделал",
    reply_markup = keyboard1)

# Функция ответа на сообщение пользователя
@bot.message_handler(content_types=['text'])
def send_text(message):
    user_choise(message.text, message.chat.id)

# Функция обработки сообщения пользователя
def user_choise(text, message_chat_id):
    if text == 'Получить график':
        bot.send_message(message_chat_id, "Выберите какой график вам необходим", reply_markup = keyboard2)
    elif text == 'Получить график выхода датчиков' or text == 'Получить график выхода АЦП' or text == 'Получить график выхода УК (устройства кодирования)' or text == 'Получить график выхода УД (устройства декодирования)':
        graphics(text, message_chat_id)
        
    elif text == 'Получить значения при тепературе ...' or text == 'Получить значение на определённой температуре' or text == 'Получить значение на отрезке температуры' or text == 'Получить все значения':
        temp_values(text, message_chat_id)
    
    elif re.match(r'(T=\d+[.]\d+)', text) or re.match(r'(T\d+[.]\d+-\d+[.]\d+)', text):
        temp_values(text, message_chat_id)
    
    elif text == 'Получить параметры датчиков температуры' or text == 'Получить параметры датчика температуры №1' or text == 'Получить параметры датчика температуры №2' or text == 'Получить параметры датчика температуры №3' or text == 'Получить параметры датчика температуры №4':
        temp_sensors_preferences(text, message_chat_id)
    
    elif text == 'Обновить значения датчиков':
        temp_sensors_refresh(message_chat_id)
    
    elif text == 'Обратно':
        bot.send_message(message_chat_id, "Пожалуйста, выберите действие, которое хотите чтобы я сделал", reply_markup = keyboard1)
    else:
        bot.send_message(message_chat_id, "Я не знаю такой команды, проверьте правильность ввода")
    
# Функция показа графика
def graphics(text, message_chat_id):
    if text == 'Получить график выхода датчиков':
        photo = open(os.path.join(os.getcwd(), 'image', 'sensors.jpg'), 'rb')
        bot.send_photo(message_chat_id, photo)
    elif text == 'Получить график выхода АЦП':
        photo = open(os.path.join(os.getcwd(), 'image', 'precode.jpg'), 'rb')
        bot.send_photo(message_chat_id, photo)
    elif text == 'Получить график выхода УК (устройства кодирования)':
        photo = open(os.path.join(os.getcwd(), 'image', 'coded.jpg'), 'rb')
        bot.send_photo(message_chat_id, photo)
    elif text == 'Получить график выхода УД (устройства декодирования)':
        photo = open(os.path.join(os.getcwd(), 'image', 'decoded.jpg'), 'rb')
        bot.send_photo(message_chat_id, photo)

# Функция получения значений при определённой температуре
def temp_values(text, message_chat_id):
    if text == 'Получить значения при тепературе ...':
        bot.send_message(message_chat_id, "Выберите какого типа значения вы бы хотели получить", reply_markup = keyboard3)
    
    elif text == 'Получить значение на определённой температуре':
        bot.send_message(message_chat_id, "Введите необходимую температуру в формате \"T=_значение_\", например: T=288.89")
    
    elif text == 'Получить значение на отрезке температуры':
        bot.send_message(message_chat_id, "Введите необходимую температуру в формате \"T_значение_-_значение_\", например: T288.5-310.94")
    
    elif re.match(r'(T=\d+[.]\d+)', text):
        tmp = float(text[2:])
        if tmp > 328 or tmp < 288:
            bot.send_message(message_chat_id, "Неправильно выбрано значение температуры")
        else:
            bot.send_message(message_chat_id, values.get_value(tmp))
    
    elif re.match(r'(T\d+[.]\d+-\d+[.]\d+)', text):
        value_range = re.split(r'-', text)
        temp_min = float(value_range[0][1:])
        temp_max = float(value_range[1])
        if temp_min > 328 or temp_max > 328 or temp_min < 288 or temp_max < 288:
            bot.send_message(message_chat_id, "Неправильно выбранный диапазон температуры")
        else:
            bot.send_message(message_chat_id, values.get_range_values(temp_min, temp_max))
    
    elif text == 'Получить все значения':
        bot.send_message(message_chat_id, "Подождите, пока произойдут расчёты")
        result = values.get_all_values()
        
        result_list1 = dict()
        result_list2 = dict()
        result_list3 = dict()
        result_list4 = dict()
        
        isFirst = True
        isSecond = True
        isThird = True
        isFourth = True
        for i in range(0, 1000, 1):
            if isFirst:
                result_list1[str(i)] = "1"
                isFirst = False
            elif isSecond:
                result_list2[str(i)] = "1"
                isSecond = False
            elif isThird:
                result_list3[str(i)] = "1"
                isThird = False
            elif isFourth:
                result_list4[str(i)] = "1"
                isFirst = True
                isSecond = True
                isThird = True
        
        result_str1 = "Значения датчика №1:\n"
        result_str2 = "Значения датчика №2:\n"
        result_str3 = "Значения датчика №3:\n"
        result_str4 = "Значения датчика №4:\n"
        for i in range(0, 1000, 1):
            if str(i) in result_list1:
                result_str1 = result_str1 + str(result[i]) + " В\n"
            elif str(i) in result_list2:
                result_str2 = result_str2 + str(result[i]) + " В\n"
            elif str(i) in result_list3:
                result_str3 = result_str3 + str(result[i]) + " В\n"
            elif str(i) in result_list4:
                result_str4 = result_str4 + str(result[i]) + " В\n"
                
            if result_str4.count("\n") > 100:
                bot.send_message(message_chat_id, result_str1)
                bot.send_message(message_chat_id, result_str2)
                bot.send_message(message_chat_id, result_str3)
                bot.send_message(message_chat_id, result_str4)
                result_str1 = "Значения датчика №1:\n"
                result_str2 = "Значения датчика №2:\n"
                result_str3 = "Значения датчика №3:\n"
                result_str4 = "Значения датчика №4:\n"
        
        bot.send_message(message_chat_id, result_str1)
        bot.send_message(message_chat_id, result_str2)
        bot.send_message(message_chat_id, result_str3)
        bot.send_message(message_chat_id, result_str4)

# Фукнция получения параметров датчиков температуры
def temp_sensors_preferences(text, message_chat_id):
    if text == 'Получить параметры датчиков температуры':
        bot.send_message(message_chat_id, 'Выберите значения какого датчика вы хотите узнать', reply_markup = keyboard4)
    elif text == 'Получить параметры датчика температуры №1':
        bot.send_message(message_chat_id,
        "Датчик №1 обладает следующими параметрами:\n" + 
        "- Минимальная температура = 228 K;\n" + 
        "- Максильманая температура = 328 K;\n" + 
        "- ТКС = -50;\n" + 
        "- R = 150 Ом;\n" + 
        "- Gain = 0.705.")
    elif text == 'Получить параметры датчика температуры №2':
        bot.send_message(message_chat_id,
        "Датчик №2 обладает следующими параметрами:\n" + 
        "- Минимальная температура = 228 K;\n" + 
        "- Максильманая температура = 328 K;\n" + 
        "- ТКС = -40;\n" + 
        "- R = 163 Ом;\n" + 
        "- Gain = 0.813.")
    elif text == 'Получить параметры датчика температуры №3':
        bot.send_message(message_chat_id,
        "Датчик №3 обладает следующими параметрами:\n" + 
        "- Минимальная температура = 228 K;\n" + 
        "- Максильманая температура = 328 K;\n" + 
        "- ТКС = -30;\n" + 
        "- R = 220 Ом;\n" + 
        "- Gain = 0.807.")
    elif text == 'Получить параметры датчика температуры №4':
        bot.send_message(message_chat_id,
        "Датчик №4 обладает следующими параметрами:\n" + 
        "- Минимальная температура = 228 K;\n" + 
        "- Максильманая температура = 328 K;\n" + 
        "- ТКС = -20;\n" + 
        "- R = 320 Ом;\n" + 
        "- Gain = 0.835")

# Функция обновления значений сенсоров
def temp_sensors_refresh(message_chat_id):
    if str(message_chat_id) != '257089707':
        bot.send_message(message_chat_id, "У вас нет прав на обновление данных")
    else:
        bot.send_message(message_chat_id, "Подождите, пока пройдёт процесс обновления данных")
        if path.exists(os.path.join(os.getcwd(), 'values', 'sensors.mat')):
            os.remove(os.path.join(os.getcwd(), 'values', 'sensors.mat'))
        runModel.run_model()
        shutil.move(os.path.join(os.getcwd(), 'sensors.mat'), os.path.join(os.getcwd(), 'values', 'sensors.mat'))
        bot.send_message(message_chat_id, "Значения обновлены")

bot.polling()
