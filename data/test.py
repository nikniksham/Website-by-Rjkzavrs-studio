from requests import get, post, delete, put

# Тесты: 1 - api/v2/user; 2 - api/v2/jobs
test_version_first = True

# методы
test_get = True
test_post = True
test_delete = True
test_put = True
if test_version_first:
    if test_post:
        print(get('http://localhost:8000/api/user/n@gmail.com/123').json())
        print(post('http://localhost:8000/api/user',
                   json={'id': 10,
                         'name': 'Николай',
                         'surname': 'Шамков',
                         'age': 16,
                         'nickname': 'nikniksham',
                         'email': 'n@gmail.com',
                         'password': '123'}).json())

    if test_get:
        print(get('http://localhost:8000/api/user/n@gmail.com/123').json())

    if test_put:
        print(put('http://localhost:8000/api/user/n@gmail.com/123', json={'age': 20}).json())
        print(get('http://localhost:8000/api/user/n@gmail.com/123').json())

    if test_delete:
        print(delete('http://localhost:8000/api/user/n@gmail.com/123').json())
        print(get('http://localhost:8000/api/user/n@gmail.com/123').json())
