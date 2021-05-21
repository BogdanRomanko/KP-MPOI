# Импортируем необходимые библиотеки для работы
# с Matlab и путями к файлам
import matlab.engine
import os

# Основная функция запуска модели на симуляцию
def run_model():
    # Запускаем Matlab для выполнения модели
    eng = matlab.engine.start_matlab()

    # Изменяем стандартный путь в Matlab на папку с проектом
    os.chdir(os.path.dirname(__file__)) 
    eng.cd(os.getcwd())

    # Запускаем скрипт m-файла на регистрацию нашей библиотеки
    # KP_lib в браузере библиотек Matlab
    ret = eng.KP_lib()

    # Запускаем модель на выполнение, в результате чего получим
    # файл sensors.mat для работы с ним
    ret = eng.sim("UK_UD")

    # Закрываем Matlab
    eng.exit()