# Импортируем библиотеки для работы с путями,
# Matlab и mat-файлами
import os
import matlab.engine

# Функция получения всех значений
def get_all_values():
    eng = matlab.engine.start_matlab()

    os.chdir(os.path.join(os.path.dirname(__file__), 'values'))
    eng.cd(os.getcwd())

    ans = eng.load('sensors.mat', 'ans')
    value_list = list(ans.get('ans')[1])
    
    return value_list

# Функция получения значений на диапазоне температур
def get_range_values(temp_min, temp_max):
    result = get_all_values()
    result_str = str()
    result_str_list = list()
    for i in range(0, 1000, 1):
        if float((i * 0.04) + 288) > temp_min and float((i * 0.04) + 288) < temp_max:
            if result_str.count('\n') > 50:
                result_str = str(result_str + "При температуре " + str((i * 0.04) + 288) + "K:\n"
                + "- Датчик №1: " + str(result[i])[0:5] + " В;\n"
                + "- Датчик №2: " + str(result[i + 1])[0:5] + " В;\n"
                + "- Датчик №3: " + str(result[i + 2])[0:5] + " В;\n"
                + "- Датчик №4: " + str(result[i + 3])[0:5] + " В.\n")
                i = i + 3
                result_str_list.append(result_str)
                result_str = ""
            else:
                result_str = str(result_str + "При температуре " + str((i * 0.04) + 288) + "K:\n"
                + "- Датчик №1: " + str(result[i])[0:5] + " В;\n"
                + "- Датчик №2: " + str(result[i + 1])[0:5] + " В;\n"
                + "- Датчик №3: " + str(result[i + 2])[0:5] + " В;\n"
                + "- Датчик №4: " + str(result[i + 3])[0:5] + " В.\n")
                i = i + 3
    
    result_str_list.insert(0, "Значения при температуре " + str(temp_min) + "-" + str(temp_max) + "K следующие:\n")
    
    return result_str_list

# Функция получения значения при определённой температуре
def get_value(temp):
    result = get_all_values()
    
    for i in range(0, 1000, 1):
        if float((i * 0.04) + 288) > temp or float((i * 0.04) + 288) == temp or i == 997:
            result_str = str("Значения при температуре " + str(temp) + "K следующие:\n" 
            + "- Датчик №1: " + str(result[i])[0:5] + " В;\n"
            + "- Датчик №2: " + str(result[i + 1])[0:5] + " В;\n"
            + "- Датчик №3: " + str(result[i + 2])[0:5] + " В;\n"
            + "- Датчик №4: " + str(result[i + 3])[0:5] + " В.")
            
            return result_str
            
    return "Произошла ошибка"

# 0.16 От 288 до 328
# 250 итераций