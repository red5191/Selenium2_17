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
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

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


print("Приветствую тебя в нашем интернет - магазине")

button_add_backpack = driver.find_element(By.XPATH, "//button[@id='add-to-cart-sauce-labs-backpack']")
button_add_bike = driver.find_element(By.XPATH, "//button[@id='add-to-cart-sauce-labs-bike-light']")
button_add_t_shirt = driver.find_element(By.XPATH, "//button[@id='add-to-cart-sauce-labs-bolt-t-shirt']")
button_add_jacket = driver.find_element(By.XPATH, "//button[@id='add-to-cart-sauce-labs-fleece-jacket']")
button_add_onesie = driver.find_element(By.XPATH, "//button[@id='add-to-cart-sauce-labs-onesie']")
button_add_t_shirt_red = driver.find_element(By.XPATH, "//*[@id='add-to-cart-test.allthethings()-t-shirt-(red)']")

value_backpack = driver.find_element(By.XPATH, "//*[@id='item_4_title_link']").text
value_bike = driver.find_element(By.XPATH, "//*[@id='item_0_title_link']").text
value_t_shirt = driver.find_element(By.XPATH, "//*[@id='item_1_title_link']").text
value_jacket = driver.find_element(By.XPATH, "//*[@id='item_5_title_link']").text
value_onesie = driver.find_element(By.XPATH, "//*[@id='item_2_title_link']").text
value_t_shirt_red = driver.find_element(By.XPATH, "//*[@id='item_3_title_link']").text

price_backpack = driver.find_element(By.XPATH, "//*[@id='inventory_container']/div/div[1]/div[2]/div[2]/div").text
price_bike = driver.find_element(By.XPATH, "//*[@id='inventory_container']/div/div[2]/div[2]/div[2]/div").text
price_t_shirt = driver.find_element(By.XPATH, "//*[@id='inventory_container']/div/div[3]/div[2]/div[2]/div").text
price_jacket = driver.find_element(By.XPATH, "//*[@id='inventory_container']/div/div[4]/div[2]/div[2]/div").text
price_onesie = driver.find_element(By.XPATH, "//*[@id='inventory_container']/div/div[5]/div[2]/div[2]/div").text
price_t_shirt_red = driver.find_element(By.XPATH, "//*[@id='inventory_container']/div/div[6]/div[2]/div[2]/div").text

merch_dict = {
'1' : [button_add_backpack, value_backpack, price_backpack],
'2' : [button_add_bike, value_bike, price_bike],
'3' : [button_add_t_shirt, value_t_shirt, price_t_shirt],
'4' : [button_add_jacket, value_jacket, price_jacket],
'5' : [button_add_onesie, value_onesie, price_onesie],
'6' : [button_add_t_shirt_red, value_t_shirt_red, price_t_shirt_red]
}

number = str(input("""Выбери один из следующих товаров и укажи его номер:
    1 - Sauce Labs Backpack
    2 - Sauce Labs Bike Light
    3 - Sauce Labs Bolt T-Shirt
    4 - Sauce Labs Fleece Jacket
    5 - Sauce Labs Onesie
    6 - Test.allTheThings() T-Shirt (Red)
    """))
while number not in merch_dict:
    print('Ты ввел что-то не то')
    number = str(input("""Выбери один из следующих товаров и укажи его номер:
1 - Sauce Labs Backpack
2 - Sauce Labs Bike Light
3 - Sauce Labs Bolt T-Shirt
4 - Sauce Labs Fleece Jacket
5 - Sauce Labs Onesie
6 - Test.allTheThings() T-Shirt (Red)
"""))

merch_dict.get(number)[0].click()

print(f'Выбран товар: {merch_dict[number][1]}')
print(f'Цена товара: {merch_dict[number][2]}')

driver.find_element(By.XPATH, "//a[@data-test='shopping-cart-link']").click()
print('Заходим в корзину')

# проверяем соответствие наименований и цен в корзине
value_cart_product = driver.find_element(By.XPATH, "//*[@data-test='inventory-item-name']").text
print(f'Товар в корзине: {value_cart_product}')
assert merch_dict[number][1] == value_cart_product, 'Наименования не соответствуют'
print('Наименование соответствует выбранному')

value_cart_price_product = driver.find_element(By.XPATH, "//*[@class='inventory_item_price']").text
print(f'Цена товара в корзине: {value_cart_price_product}')
assert merch_dict[number][2] == value_cart_price_product, 'Цены не соответствуют'
print('Цена соответствует')

# переходим по кнопке "Checkout", вводим данные заказчика и переходим по кнопке "Continue"
checkout = driver.find_element(By.XPATH, "//*[@id='checkout']")
checkout.click()
print('Нажимаем кнопку Checkout')

fake = Faker('en_US')

first_name = driver.find_element(By.XPATH, "//input[@id='first-name']")
first_name.send_keys(fake.first_name())
print('Генерируем имя')

last_name = driver.find_element(By.XPATH, "//input[@id='last-name']")
last_name.send_keys(fake.last_name())
print('Генерируем фамилию')

postal_code = driver.find_element(By.XPATH, "//input[@id='postal-code']")
postal_code.send_keys(fake.postalcode())
print('Генерируем индекс')

button_continue = driver.find_element(By.XPATH, "//input[@id='continue']")
button_continue.click()
print('Нажимаем Continue')

# Сверяем наименования и цены на финальной странице оформления заказа
value_final_product = driver.find_element(By.XPATH, "//*[@class='inventory_item_name']").text
print(f'Финальное наименование товара: {value_final_product}')
assert merch_dict[number][1] == value_final_product, 'Наименования не соответствуют'
print('Финальное наименование товара соответствует выбранному')

value_final_price_product = driver.find_element(By.XPATH, "//*[@class='inventory_item_price']").text
print(f'Финальная цена товара: {value_final_price_product}')
assert merch_dict[number][2] == value_final_price_product, 'Цены не соответствуют'
print('Цены соответствуют')

# завершаем оформление заказа и удостоверяемся что находимся на нужной странице
button_finish = driver.find_element(By.XPATH, "//*[@id='finish']")
button_finish.click()
print('Нажимаем кнопку Finish')

value_checkout_complete = driver.find_element(By.XPATH, "//*[contains(text(), 'Thank you for your order!')]").text
print(f'Текст на странице: {value_checkout_complete}')
assert value_checkout_complete == 'Thank you for your order!'
print('Заказ успешно завершен')

# после задержки в 10 секунд закрываем браузер
time.sleep(10)
driver.quit()