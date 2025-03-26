from requests import get, post, delete
from pprint import pprint

#  корректный запрос
pprint(get('http://localhost:8080/api/v2/jobs').json())

#  нет такого id
print(get('http://localhost:8080/api/v2/jobs/999').json())

#  посылаем строку вместо числа
print(get('http://localhost:8080/api/v2/jobs/BlaBlaBlaBleBleBleBluBluBlu').json())

#  корректный запрос
print(get('http://localhost:8080/api/v2/jobs/9').json())

#  пустой json
print(post('http://localhost:8080/api/v2/jobs', json={}).json())

#  корректный запрос
print(post('http://localhost:8080/api/v2/jobs', json={'team_leader': 2,
                                                      'job': 'Важная работа',
                                                      'work_size': 10,
                                                      'collaborators': '3, 4, 5',
                                                      'is_finished': False}).json())

# работы с id = 999 нет в базе
# УШАТАЙТЕ МЕНЯ БОЛГАРКОЙ, Я ЗДЕСЬ ОШИБКУ ТРИ ДНЯ ИСКАЛ, ОКАЗАЛОСЬ, ЧТО В АДРЕСЕ ".../v2/..." ЗАБЫЛ
print(delete('http://localhost:8080/api/v2/jobs/999').json())

#  вместо id отправляем строку
print(delete('http://localhost:8080/api/v2/jobs/BlaBlaBlaBleBleBleBluBluBlu').json())

#  корректный запрос
print(delete('http://localhost:8080/api/v2/jobs/19').json())
