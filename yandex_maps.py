import sys

import requests


def search(toponym):
    try:
        toponym_to_find = toponym

        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
            "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
            "geocode": toponym_to_find,
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)

        if not response:
            # обработка ошибочной ситуации
            print('ERROR')
            return

        # Преобразуем ответ в json-объект
        json_response = response.json()
        # Получаем первый топоним из ответа геокодера.
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        ll = ','.join(toponym['Point']['pos'].split(' '))
        left_corner = toponym['boundedBy']['Envelope']['upperCorner']
        right_corner = toponym['boundedBy']['Envelope']['lowerCorner']
        scale = min(float(left_corner.split(' ')[0]) - float(right_corner.split(' ')[0]),
                    float(left_corner.split(' ')[1]) - float(right_corner.split(' ')[1]))
        spn = f"{scale},{scale}"
        return tuple([ll, spn])
    except Exception:
        print('ERROR')


def get_image(ll, spn):
    server_address = 'https://static-maps.yandex.ru/v1?'
    api_key = 'af90eac0-d94c-489a-8b0a-7cc38740ab4b'
    ll_spn = f'll={ll}&spn={spn}'
    map_request = f"{server_address}{ll_spn}"
    map_request += f"&apikey={api_key}"
    map_request += "&style=tags.all:terrain"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "./static/images/map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
