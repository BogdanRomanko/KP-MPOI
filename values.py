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
    
    return temp_max

# Функция получения значения при определённой температуре
def get_value(temp):
    value_list = get_all_values()
    
    return temp

#0.16 От 288

