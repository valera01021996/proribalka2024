import requests
from requests.auth import HTTPBasicAuth
import os
import time
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
from requests import Session
import pymysql

load_dotenv()

base_url = "https://api.moysklad.ru/api/remap/1.2/report/stock/all"
# connection, cursor = connect_to_database()
auth_credentials = HTTPBasicAuth(os.getenv("LOGIN_MOYSKLAD"), os.getenv("PASSWORD_MOYSKLAD"))

received_product_ids = []


def connect_to_database() -> tuple:
    connection = pymysql.connect(
        host="localhost",
        database="proribalka",
        user="proribalka",
        password="twix3327348"
    )
    cursor = connection.cursor()
    return connection, cursor


connection, cursor = connect_to_database()


def setup_session():
    session = Session()
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET", "POST"]  # Используйте allowed_methods вместо method_whitelist для новых версий
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session


session = setup_session()


def add_or_replace_to_products(product_id, product_name, image, price, quantity, description, category_name,
                               subcategory_name, brand_name, serie_name, type_name):
    try:
        cursor.execute(f"""INSERT INTO products_bu (product_id, product_name, image, price, quantity, description, category_name,
         subcategory_name, brand_name, serie_name, type_name)
                VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                product_name= VALUES(product_name),
                description= VALUES(description),
                image= VALUES(image),
                price= VALUES(price),
                quantity= VALUES(quantity),
                category_name= VALUES(category_name),
                subcategory_name= VALUES(subcategory_name),
                brand_name= VALUES (brand_name),
                serie_name= VALUES (serie_name),
                type_name= VALUES (type_name)
            """, (
            product_id, product_name, image, price, quantity, description, category_name, subcategory_name, brand_name,
            serie_name, type_name))

    except Exception as ex:
        print(ex)
    else:
        connection.commit()


def get_photo(url: str, title: str):
    try:
        response = session.get(url, auth=auth_credentials, timeout=(10, 30))
        image = response.content
        if "/" in title:
            title = title.replace("/", " ")
        if "\"" in title:
            title = title.replace("\"", "")
        with open(f"media/images/{title}.jpg", "wb") as file:
            file.write(image)
        path = os.path.abspath(f"media/images/{title}.jpg")
        return path
    except:
        pass


def fetch_data(url):
    received_product_ids.clear()
    # while True:
    while url:
        response = session.get(url, auth=auth_credentials, timeout=(10, 30))

        data = response.json()
        for dict_ in data["rows"]:
            if "Б/У" in dict_["folder"]["pathName"] in dict_["folder"]["pathName"]:
                if "Приманки" in dict_["folder"]["pathName"]:
                    continue
                """Для получения описания продукта и фото след три переменные"""
                product_id = dict_["meta"]["href"].split("/")[-1]
                received_product_ids.append(product_id)
                product_url = f"https://api.moysklad.ru/api/remap/1.2/entity/product/{product_id}"
                product_response = session.get(product_url, auth=auth_credentials, timeout=(10, 30))
                """___________________________________________________________"""

                pathname_splitted = dict_["folder"]["pathName"][22:].split("/")
                last_directory = dict_["folder"]["name"]
                product_name = dict_["name"]
                price = dict_["salePrice"] // 100
                quantity = dict_["stock"]
                category_name = ""
                subcategory_name = ""
                brand_name = ""
                serie_name = ""
                type_name = ""
                description = ""
                image = ""

                """Получаем описание и фотографию"""
                if product_response.status_code == 200:
                    print("Success")
                    product_details = product_response.json()
                    description = product_details.get("description", "")
                    image_url = product_details.get("images", {}).get("meta", {}).get("href")
                    try:
                        image_url_download = \
                            session.get(image_url, auth=auth_credentials, timeout=(10, 30)).json()["rows"][0].get(
                                "meta",
                                {}).get("downloadHref", {})

                        image = get_photo(image_url_download, product_name)
                    except Exception as ex:
                        print(f"Ошибка при получении фото {ex}")
                """__________________________________________"""

                if len(pathname_splitted) == 1 and pathname_splitted[0] != "Приманки":
                    category_name = pathname_splitted[0]
                    brand_name = last_directory


                elif len(pathname_splitted) == 1 and pathname_splitted[0] == "Приманки":
                    category_name = pathname_splitted[0]
                    subcategory_name = last_directory

                elif len(pathname_splitted) == 2:
                    category_name = pathname_splitted[0]
                    brand_name = pathname_splitted[1]
                    serie_name = last_directory

                add_or_replace_to_products(product_id, product_name, image, price, quantity, description,
                                           category_name,
                                           subcategory_name, brand_name, serie_name, type_name)
        try:
            url = data["meta"]["nextHref"]
            print(url)
        except KeyError:
            print("Достигнут конец данных, нет следующей страницы")
            break


# fetch_data(base_url)

def remove_missing_products():
    try:
        if received_product_ids:  # Убедимся, что список не пустой
            received_product_ids_str = ','.join(f"'{product_id}'" for product_id in received_product_ids)
            cursor.execute(f"DELETE FROM products_bu WHERE product_id NOT IN ({received_product_ids_str})")
            print("Удалены товары, которых нет в полученных данных")
        else:
            print("Нет товаров для удаления")
    except Exception as ex:
        print(f"Ошибка при удалении товаров: {ex}")
    else:
        connection.commit()


# Основной цикл обновления базы данных
def run_update_loop(interval=600):  # Интервал обновления в секундах (10 минут по умолчанию)
    while True:
        print("Начало обновления базы данных...")
        fetch_data(base_url)  # Получаем данные с API
        remove_missing_products()  # Удаляем отсутствующие товары
        print(f"База данных обновлена. Ожидание {interval} секунд до следующего обновления.")
        time.sleep(interval)  # Задержка перед следующим обновлением


# Запуск цикла обновления
run_update_loop()
