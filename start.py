#imports 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
import time
from fake_useragent import UserAgent #for fake-useragent in chrome

#def for start
def start():
    print("App started...")
    telephone = input("telephone: \n")
    auth(telephone)

#def for auth in wb acc
def auth(telephone):
    print("Autorization...")
    ua = UserAgent()
    user_agent = ua.random
    service = Service("webdriver/chromedriver.exe")
    options = Options()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--headless") #hide browser
    driver = webdriver.Chrome(service=service,options=options)
    driver.get("https://www.wildberries.ru/security/login?returnUrl=https%3A%2F%2Fwww.wildberries.ru%2F")
    driver.maximize_window()
    print("Wb is open!")
    try:
        phone_input = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.CLASS_NAME, "input-item"))
        )
        phone_input.send_keys(telephone)
        auth_button = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.ID, "requestCode"))
        )
        auth_button.click()

        code_inputs = WebDriverWait(driver, 30).until(
            ec.visibility_of_all_elements_located((By.CLASS_NAME, "char-input__item"))
        )
        print("Please enter the code.")
        sms_code = input("code: ")

        if len(sms_code) == len(code_inputs):
            for i in range(len(sms_code)):
                code_inputs[i].send_keys(sms_code[i])
                time.sleep(0.5)  
        else:
            print(f"Error: Expected {len(code_inputs)} digits, but got {len(sms_code)}.")
        print("Main...")
        while True:
            kode = input("Enter kode for search: ").strip().lower()
            search_field = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((By.ID, "searchInput"))
            )
            search_field.send_keys(kode)
            search_field.send_keys(Keys.RETURN)
            time.sleep(3)
            print(f"Search tovar kode: {kode}")

            main_button = WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.CLASS_NAME, "breadcrumbs__back"))
            )
            main_button.click()
            print("Button main click.")
            time.sleep(3)

    except Exception as e:
        print(e)
        driver.quit()

#calling the start function
if __name__ == "__main__":
    start()

    