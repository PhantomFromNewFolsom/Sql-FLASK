from requests import get, post, delete, put
from pprint import pprint

pprint(get('http://localhost:8080/api/users').json())

pprint(get('http://localhost:8080/api/users/2').json())

#  работы с таким id не существует
print(get('http://localhost:8080/api/users/20234234903490').json())

#  вместо номера посылаем строку
print(get('http://localhost:8080/api/users/BlaBlaBlaBleBleBleBluBluBlu').json())

#  пустой запрос, ничего отправляем
print(post('http://localhost:8080/api/users', json={}).json())

#  неполный запрос, не хватает полей
print(post('http://localhost:8080/api/users',
           json={'job': 'РАБОТААА'}).json())

print(post('http://localhost:8080/api/users',
           json={'surname': 'Захаров',
                 'name': 'Захар',
                 'age': 80,
                 'position': 'Старшина',
                 'speciality': 'Ударник палками',
                 'address': 'module_4',
                 'email': 'BobrKurva@mail.ru'}).json())

#  проверяем, добавилась ли работа
pprint(get('http://localhost:8080/api/users').json())

# работы с id = 999 нет в базе
print(delete('http://localhost:8080/api/users/999').json())

#  вместо id отправляем строку
print(delete('http://localhost:8080/api/users/bold').json())

#  корректный запрос
print(delete('http://localhost:8080/api/users/23').json())

#  проверяем, удалилась ли работа
pprint(get('http://localhost:8080/api/users').json())

#  отправляем пустой запрос
print(put('http://localhost:8080/api/users/9', json={}).json())

#  отправляем неполный запрос
print(put('http://localhost:8080/api/users/9', json={'team_leader': 1}).json())

#  отправляем строку в качестве id
print(put('http://localhost:8080/api/users/BlaBlaBla', json={'team_leader': 1}).json())

print(put('http://localhost:8080/api/users/21', json={'surname': 'Захаров',
                                                      'name': 'Захар',
                                                      'age': 80,
                                                      'position': 'Старшина',
                                                      'speciality': 'Ударник палками',
                                                      'address': 'module_4',
                                                      'email': 'BobrKurva@mail.ru'}).json())

#  проверяем, изменилась ли работа
pprint(get('http://localhost:8080/api/users').json())
