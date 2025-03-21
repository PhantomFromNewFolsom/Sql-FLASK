from requests import get, post

print(get('http://localhost:8080/api/jobs').json())

print(get('http://localhost:8080/api/jobs/2').json())

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
print(get('http://localhost:8080/api/jobs').json())
