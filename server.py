# Imports
from playwright.sync_api import sync_playwright
from fake_useragent import UserAgent
import time
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

# Global kode = ""
kode = ""

# Start function
def start():
    print("Запуск приложения...")
    telephone = input("Введите номер телефона: \n")  
    auth(telephone)  

# Auth function for login
def auth(telephone):
    global kode  
    print("Авторизация...")
    ua = UserAgent()  
    user_agent = ua.random  

    with sync_playwright() as p: 
        browser = p.chromium.launch(headless=True)  # false hiden true not hiden
        context = browser.new_context(user_agent=user_agent)  
        page = context.new_page()  
        
        # Open wb
        page.goto("https://www.wildberries.ru/security/login?returnUrl=https%3A%2F%2Fwww.wildberries.ru%2F")
        page.set_viewport_size({"width": 1280, "height": 800}) 
        print("Сайт открыт!")

        try:
            phone_input = page.locator(".input-item")  
            phone_input.fill(telephone)  

            auth_button = page.locator("#requestCode")  
            auth_button.click() 

            code_inputs = page.locator(".char-input__item")  
            print("Введите код из СМС.")
            sms_code = input("Код: ")  

            # auth with code sms
            code_input_elements = page.locator(".char-input__item")  
            if code_input_elements.count() == len(sms_code):  
                for i in range(len(sms_code)):
                    code_input_elements.nth(i).fill(sms_code[i])  
                    time.sleep(0.5) 
            else:
                print(f"Ошибка: ожидалось {code_input_elements.count()} цифр, а введено {len(sms_code)}.")
            print("Авторизация завершена! Ищем товар...")

            while True:
                if kode:
                    # Search
                    search_field = page.locator("#searchInput")  
                    search_field.fill(kode)  
                    search_field.press("Enter")  
                    time.sleep(7)  
                    print(f"Ищу товар с кодом: {kode}")

                    # Add to order
                    try:
                        add_to_cart_button = page.wait_for_selector(".order__button:not(.hide)", state="visible", timeout=30000)
                        add_to_cart_button.click()  
                        print("Добавлено в корзину!")                 
                        page.goto("https://www.wildberries.ru/")  
                        print("Вернулись на главную страницу.")
                        # Reset kode
                        kode = ""  
                    except Exception as e:
                        print(f"Ошибка: {e}")
                
                time.sleep(2)  

        except Exception as e:
            print(f"Ошибка в процессе: {e}")
        finally:
            browser.close()  

# API for kode
@app.route('/kode', methods=['POST'])
def find_kode():
    global kode 
    # Get JSON
    data = request.get_json()
    kode = data.get('kode')

    # Checking kode
    if str(kode).isdigit():
        # Update kode
        kode = str(kode)
        return jsonify({"message": "Такой код есть!"}), 200
    else:
        return jsonify({"error": "Некорректное код."}), 400

# start app 
def run_flask():
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    # Run Flask server
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    start()
