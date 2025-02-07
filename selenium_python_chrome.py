# Прописываем в терминале:
# python -m pip install --upgrade pip (Обновление менеджера пакетов pip)
# pip install selenium (Устанавливаем библиотеку selenium)
# pip install webdriver-manager (Устанавливаем webdriver-manager)
# pip3 install faker (Устанавливаем библиотеку faker)

# импортируем необходимые библиотеки и элементы
import time
# from datetime import datetime, timedelta
from faker import Faker
from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver import ActionChains
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


# объявляем функции
def item_info(number):
    add_button = driver.find_element(By.XPATH, locator_dict[number][0])
    add_button.click()
    value = driver.find_element(By.XPATH, locator_dict[number][1]).text
    price = driver.find_element(By.XPATH, locator_dict[number][2]).text
    print(f'''Выбран товар: {value}
Цена товара: {price}''')
    return [value, price]


def value_price_check(info_list):
    value_check = driver.find_element(By.XPATH, "//*[@class='inventory_item_name']").text
    print(f'Наименование на проверяемой странице: {value_check}')
    assert info_list[0] == value_check, 'Наименования не соответствуют'
    print('Наименование соответствует выбранному')

    price_check = driver.find_element(By.XPATH, "//*[@class='inventory_item_price']").text
    print(f'Цена товара на проверяемой странице: {price_check}')
    assert info_list[1] == price_check, 'Цены не соответствуют'
    print('Цена соответствует')


# создаем и настраиваем экземпляр driver класса webdriver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach",True)
options.add_argument('--headless')
driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))

# создаем переменную содержащую базовую ссылку и открываем её с помощью созданного ранее driver
base_url = 'https://www.saucedemo.com/'
driver.get(base_url)
driver.maximize_window()

# вводим логин и пароль, авторизовываемся
user_name = driver.find_element(By.XPATH, "//*[@id='user-name']")
user_name.send_keys('standard_user')
password = driver.find_element(By.NAME , "password")
password.send_keys('secret_sauce')
password.send_keys(Keys.ENTER)

# создаем словарь локаторов
locator_dict = {
'1' : ["//button[@id='add-to-cart-sauce-labs-backpack']", "//*[@id='item_4_title_link']", "//*[@id='inventory_container']/div/div[1]/div[2]/div[2]/div"],
'2' : ["//button[@id='add-to-cart-sauce-labs-bike-light']", "//*[@id='item_0_title_link']", "//*[@id='inventory_container']/div/div[2]/div[2]/div[2]/div"],
'3' : ["//button[@id='add-to-cart-sauce-labs-bolt-t-shirt']", "//*[@id='item_1_title_link']", "//*[@id='inventory_container']/div/div[3]/div[2]/div[2]/div"],
'4' : ["//button[@id='add-to-cart-sauce-labs-fleece-jacket']", "//*[@id='item_5_title_link']", "//*[@id='inventory_container']/div/div[4]/div[2]/div[2]/div"],
'5' : ["//button[@id='add-to-cart-sauce-labs-onesie']", "//*[@id='item_2_title_link']", "//*[@id='inventory_container']/div/div[5]/div[2]/div[2]/div"],
'6' : ["//*[@id='add-to-cart-test.allthethings()-t-shirt-(red)']", "//*[@id='item_3_title_link']", "//*[@id='inventory_container']/div/div[6]/div[2]/div[2]/div"]
}

# запускаем меню выбора товара
print("Приветствую тебя в нашем интернет - магазине")

choice = str(input("""Выбери один из следующих товаров и укажи его номер:
    1 - Sauce Labs Backpack
    2 - Sauce Labs Bike Light
    3 - Sauce Labs Bolt T-Shirt
    4 - Sauce Labs Fleece Jacket
    5 - Sauce Labs Onesie
    6 - Test.allTheThings() T-Shirt (Red)
    """))
while choice not in locator_dict:
    print('Ты ввел что-то не то')
    choice = str(input("""Выбери один из следующих товаров и укажи его номер:
1 - Sauce Labs Backpack
2 - Sauce Labs Bike Light
3 - Sauce Labs Bolt T-Shirt
4 - Sauce Labs Fleece Jacket
5 - Sauce Labs Onesie
6 - Test.allTheThings() T-Shirt (Red)
"""))

item_info_list = item_info(choice)

# переходим в корзину
driver.find_element(By.XPATH, "//a[@data-test='shopping-cart-link']").click()
print('Переходим в корзину')

# проверяем соответствие наименований и цен в корзине
value_price_check(item_info_list)

# переходим по кнопке "Checkout", вводим данные заказчика и переходим по кнопке "Continue"
driver.find_element(By.XPATH, "//*[@id='checkout']").click()
print('Нажимаем кнопку Checkout')

fake = Faker('en_US')

driver.find_element(By.XPATH, "//input[@id='first-name']").send_keys(fake.first_name())
print('Генерируем имя')

driver.find_element(By.XPATH, "//input[@id='last-name']").send_keys(fake.last_name())
print('Генерируем фамилию')

driver.find_element(By.XPATH, "//input[@id='postal-code']").send_keys(fake.postalcode())
print('Генерируем индекс')

driver.find_element(By.XPATH, "//input[@id='continue']").click()
print('Нажимаем Continue')

# сверяем наименования и цены на финальной странице оформления заказа
value_price_check(item_info_list)

# завершаем оформление заказа и удостоверяемся что находимся на нужной странице
driver.find_element(By.XPATH, "//*[@id='finish']").click()
print('Нажимаем кнопку Finish')

value_checkout_complete = driver.find_element(By.XPATH, "//*[contains(text(), 'Thank you for your order!')]").text
print(f'Текст на странице: {value_checkout_complete}')
assert value_checkout_complete == 'Thank you for your order!'
print('Заказ успешно завершен')

# после задержки в 10 секунд закрываем браузер
time.sleep(10)
driver.quit()