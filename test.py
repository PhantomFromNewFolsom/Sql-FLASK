from requests import get, post

print(get('http://localhost:8080/api/jobs').json())

print(get('http://localhost:8080/api/jobs/2').json())

print(get('http://localhost:8080/api/jobs/20234234903490').json())

print(get('http://localhost:8080/api/jobs/BlaBlaBlaBleBleBleBluBluBlu').json())

print(post('http://localhost:8080/api/jobs', json={}).json())

print(post('http://localhost:8080/api/jobs',
           json={'title': 'Заголовок'}).json())

print(post('http://localhost:8080/api/jobs',
           json={'team_leader': 2,
                 'job': 'Важная работа',
                 'work_size': 10,
                 'collaborators': '3, 4, 5',
                 'start_date': [2025, 3, 18],
                 'end_date': [2025, 3, 18],
                 'is_finished': False}).json())
