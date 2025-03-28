from requests import get, post, delete, put
from pprint import pprint

pprint(get('http://localhost:8080/api/jobs').json())

pprint(get('http://localhost:8080/api/jobs/2').json())

#  работы с таким id не существует
print(get('http://localhost:8080/api/jobs/20234234903490').json())

#  вместо номера посылаем строку
print(get('http://localhost:8080/api/jobs/BlaBlaBlaBleBleBleBluBluBlu').json())

#  пустой запрос, ничего отправляем
print(post('http://localhost:8080/api/jobs', json={}).json())

#  неполный запрос, не хватает полей
print(post('http://localhost:8080/api/jobs',
           json={'job': 'РАБОТААА'}).json())

print(post('http://localhost:8080/api/jobs',
           json={'team_leader': 2,
                 'job': 'Важная работа',
                 'work_size': 10,
                 'collaborators': '3, 4, 5',
                 'start_date': [2025, 3, 18],
                 'end_date': [2025, 3, 18],
                 'is_finished': False}).json())

#  проверяем, добавилась ли работа
pprint(get('http://localhost:8080/api/jobs').json())

# работы с id = 999 нет в базе
print(delete('http://localhost:8080/api/jobs/999').json())

#  вместо id отправляем строку
print(delete('http://localhost:8080/api/jobs/bold').json())

#  корректный запрос
print(delete('http://localhost:8080/api/jobs/10').json())

#  проверяем, удалилась ли работа
pprint(get('http://localhost:8080/api/jobs').json())

#  отправляем пустой запрос
print(put('http://localhost:8080/api/jobs/9', json={}).json())

#  отправляем неполный запрос
print(put('http://localhost:8080/api/jobs/9', json={'team_leader': 1}).json())

#  отправляем строку в качестве id
print(put('http://localhost:8080/api/jobs/BlaBlaBla', json={'team_leader': 1}).json())

print(put('http://localhost:8080/api/jobs/9', json={'team_leader': 1,
                                                    'job': 'Отрабатывание барщины',
                                                    'work_size': 100,
                                                    'collaborators': '3, 4, 5, 6, 7 , 8',
                                                    'start_date': [2025, 3, 21],
                                                    'end_date': [2025, 3, 21],
                                                    'is_finished': True}).json())

#  проверяем, изменилась ли работа
pprint(get('http://localhost:8080/api/jobs').json())
