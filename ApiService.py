import json
import requests
import sqlite3 as sl

#Создание/подключение к БД
STR_CONNECTION = sl.connect('ConfigApp.db')

# Создаем курсор
cursor = STR_CONNECTION.cursor()

#Получаем данные из таблицы
cursor.execute("SELECT * FROM Config")
result = cursor.fetchall()

#Базовый URL для запросов
BASE_URL = result[0][1]

#Сюда API токен с сайта
API_KEY =  result[0][2]

#Язык ответа
LANGUAGE = result[0][3]

#Смена языка
def setLanguage():
    inputText = input("Выберите язык введя его цифру: \n1 - Ru\n2 - En\n\r")
    while True:
        match inputText:
            case '1': 
                LANGUAGE = 'ru'
                break
            case '2': 
                LANGUAGE = 'en'
                break
            case _:
                inputText = input("Введено неверное число! Введите 1 или 2\n\r")
    updateLanguageDb(LANGUAGE)

#Смена Api 
def setApiKey():
    API_KEY = input("Укажите Api ключ DADATA: ")
    updateApiKeyDb(API_KEY)

#Обновление Api в БД
def updateApiKeyDb(data):
    sql = """
    UPDATE Config 
    SET ApiKey = ?
    WHERE Id = 1
    """
    
    cursor.execute(sql,(data,))
    STR_CONNECTION.commit()
    input("Изменения вступят в силу после перезапуска. Нажмите ввод для выхода")
    exit()

#Обновление языка в БД
def updateLanguageDb(data):
    sql = """
    UPDATE Config 
    SET Language = ?
    WHERE Id = 1
    """
    
    cursor.execute(sql,(data,))
    STR_CONNECTION.commit()
    start()

#Авторизация, отправка запроса и получение ответа
def findAddress(query):
    headers = {
        'Authorization': 'Token ' + result[0][2],
        'Content-Type': 'application/json',
        'Accept':'application/json'
    }
    data = {
        'query': query,
        'language': result[0][3]
    }
    res = requests.post(result[0][1], data=json.dumps(data), headers=headers)
    return res.json()

#Смена настроек
def options():
    inputText = input("1 - смениь язык\n2 - сменить Api\n3 - вернуться\n\r")
    match inputText:
        case '1':
            setLanguage() 
        case '2':
            setApiKey()
        case '3':
            start()
        case _: options()

#Начало
def start():
    if API_KEY == 'default':
        setApiKey()
    while True:
        #Вывод ответа
        data = input("Введите адрес:\n\r")
        data = findAddress(data)
        while True:
        
            if len(data['suggestions']) == 0:
                print("\nАдрес не найден")
                data = input("Введите адрес:\n\r")
                data = findAddress(data)

            elif len(data['suggestions']) == 1:
                
                print("\nШирина: ", data['suggestions'][0]['data']['geo_lat'], "\n")
                print("Долгота: ", data['suggestions'][0]['data']['geo_lon'], "\n")  
                break  
            else:
                i = 0
                while i < len(data['suggestions']):
                    print(i+1, data['suggestions'][i]['value'])
                    i+=1
                i = input("\nУточните адрес введя его номер\n\r")
                i = int(i)
                data = findAddress(data['suggestions'][i-1]['value'])
                

        while True:
            inputText = input("Для продолжения введите 'y', для выхода введите 'n', для перехода к настройкам введите 's'\n\r")
            if inputText == 'n' or inputText == 'N':
                cursor.close()
                STR_CONNECTION.close()
                exit()
            elif inputText == 's' or inputText == 'S':
                options()
            elif inputText == 'y' or inputText == 'Y':
                break

start()


        





