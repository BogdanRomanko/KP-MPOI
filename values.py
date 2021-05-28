# Импортируем библиотеки для работы с путями,
# Matlab и mat-файлами
import os
import matlab.engine

# Функция получения всех значений
def get_all_values():
    # Запускаем Matlab
    eng = matlab.engine.start_matlab()
    
    # меняем рабочую директорию для корректной работы Matlab
    os.chdir(os.path.join(os.path.dirname(__file__), 'values'))
    eng.cd(os.getcwd())
    
    # Загружаем файл со значениями в переменную ans
    ans = eng.load('sensors.mat', 'ans')
    
    # Закрываем Matlab
    eng.exit()
    
    # Преобразуем полученные значения в список
    value_list = list(ans.get('ans')[1])
    
    # Возвращаем список с данными
    return value_list

# Функция получения значений на диапазоне температур
def get_range_values(temp_min, temp_max):
    # Получаем все значения
    result = get_all_values()
    
    # Создаём переменные строку и список для записи данных
    result_str = str()
    result_str_list = list()
    
    #Проходимся по всем итерациям при указанных температурах
    for i in range(0, 1000, 1):
        if float((i * 0.04) + 288) > temp_min and float((i * 0.04) + 288) < temp_max:
            # Если накопилось свыше 50 строк - добавляем строку в список
            # и очищаем её для дальнейшей записи
            if result_str.count('\n') > 50:
                result_str = str(result_str + "При температуре " + str((i * 0.04) + 288) + "K:\n"
                + "- Датчик №1: " + str(result[i])[0:5] + " В;\n"
                + "- Датчик №2: " + str(result[i + 1])[0:5] + " В;\n"
                + "- Датчик №3: " + str(result[i + 2])[0:5] + " В;\n"
                + "- Датчик №4: " + str(result[i + 3])[0:5] + " В.\n")
                i = i + 3
                result_str_list.append(result_str)
                result_str = ""
            # Если в строке менее 50 переносов строк, то дальше считываем в неё данные
            else:
                result_str = str(result_str + "При температуре " + str((i * 0.04) + 288) + "K:\n"
                + "- Датчик №1: " + str(result[i])[0:5] + " В;\n"
                + "- Датчик №2: " + str(result[i + 1])[0:5] + " В;\n"
                + "- Датчик №3: " + str(result[i + 2])[0:5] + " В;\n"
                + "- Датчик №4: " + str(result[i + 3])[0:5] + " В.\n")
                i = i + 3
    
    # Добавяем первую строку в список и возвращаем его
    result_str_list.insert(0, "Значения при температуре " + str(temp_min) + "-" + str(temp_max) + "K следующие:\n")
    
    return result_str_list

# Функция получения значения при определённой температуре
def get_value(temp):
    # Получаем все значения
    result = get_all_values()
    
    # На всех итерациях проверяем достигнута ли нужная температура
    for i in range(0, 1000, 1):
        # Если нужная температура достигнута - записываем её и возвращаем
        if float((i * 0.04) + 288) > temp or float((i * 0.04) + 288) == temp or i == 997:
            result_str = str("Значения при температуре " + str(temp) + "K следующие:\n" 
            + "- Датчик №1: " + str(result[i])[0:5] + " В;\n"
            + "- Датчик №2: " + str(result[i + 1])[0:5] + " В;\n"
            + "- Датчик №3: " + str(result[i + 2])[0:5] + " В;\n"
            + "- Датчик №4: " + str(result[i + 3])[0:5] + " В.")
            
            return result_str
    
    # Если данная температура не была обнаружена - возвращаем ошибку
    return "Произошла ошибка"
