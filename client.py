import requests

while True:
    # Вводим код 
    kode = input("Введите код (или 'exit' для выхода): ")

    # Выход из цикла
    if kode.lower() == 'exit':
        print("Выход из программы.")
        break

    # Проверяем код
    if not kode.isdigit():
        print("Ошибка! Введите нормальный код.")
        continue

    # Отправляем код на сервер
    url = 'http://127.0.0.1:5000/kode'  
    data = {'kode': kode}

    # Выполняем POST-запрос
    response = requests.post(url, json=data)

    # Выводим ответ сервера
    if response.status_code == 200:
        print(response.json()['message'])
    else:
        print(response.json()['error'])
