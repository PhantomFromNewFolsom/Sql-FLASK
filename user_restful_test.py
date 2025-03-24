from requests import get, post, delete
from pprint import pprint

#  корректный запрос
pprint(get('http://localhost:8080/api/v2/users').json())

#  нет такого id
print(get('http://localhost:8080/api/v2/users/999').json())

#  посылаем строку вместо числа
print(get('http://localhost:8080/api/v2/users/BlaBlaBlaBleBleBleBluBluBlu').json())

#  корректный запрос
print(get('http://localhost:8080/api/v2/users/9').json())

#  пустой json
print(post('http://localhost:8080/api/v2/users', json={}).json())

#  корректный запрос
print(post('http://localhost:8080/api/v2/users', json={'surname': 'Захаров',
                                                       'name': 'Захар',
                                                       'age': 80,
                                                       'position': 'Старшина',
                                                       'speciality': 'Ударник палками',
                                                       'address': 'module_4',
                                                       'email': 'BlEEEEr@mail.ru'}).json())

# работы с id = 999 нет в базе
print(delete('http://localhost:8080/api/users/999').json())

#  вместо id отправляем строку
print(delete('http://localhost:8080/api/users/BlaBlaBlaBleBleBleBluBluBlu').json())

#  корректный запрос
print(delete('http://localhost:8080/api/users/23').json())
