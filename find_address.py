import requests
import os
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("TOKEN_GEOCODING")


async def get_address_via_coords(coords: str):
    params = {
        "apikey": TOKEN,
        "format": "json",
        "lang": "ru_RU",
        "kind": "house",
        "geocode": coords
    }
    try:
        response = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=params)
        json_data = response.json()
        address = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
        return address

    except Exception as e:
        return 'ERROR'

