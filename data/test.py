from requests import get, post, delete, put

test_version_first = False
test_version_second = True

link_website = 'https://rjkzavrs-studio.herokuapp.com/'
link_website_2 = 'http://localhost:8000/'
test_get = True
test_post = True
test_delete = True
test_put = True
if test_version_first:
    if test_post:
        print(get(f'{link_website_2}api/user/n@gmail.com/1234567q').json())
        print(post(f'{link_website_2}api/user',
                   json={'id': 10,
                         'name': 'Николай',
                         'surname': 'Шамков',
                         'age': 16,
                         'nickname': 'nikniksham',
                         'email': 'n@gmail.com',
                         'password': '1234567q'}).json())

    if test_get:
        print(get(f'{link_website_2}api/user/n@gmail.com/1234567q').json())

    if test_put:
        print(put(f'{link_website_2}api/user/n@gmail.com/1234567q', json={'age': 20}).json())
        print(get(f'{link_website_2}api/user/n@gmail.com/1234567q').json())

    if test_delete:
        print(delete(f'{link_website_2}api/user/n@gmail.com/1234567q').json())
        print(get(f'{link_website_2}api/user/n@gmail.com/1234567q').json())

if test_version_second:
    if test_post:
        print(get(f'{link_website_2}api/developers_diary_admin/test@yandex.ru/test_123/10').json())
        print(post(f'{link_website_2}api/developers_diary_admin_create/test@yandex.ru/test_123',
                   json={'id': 10,
                         'header': 'Тестовая запись',
                         'body': 'Тестовая запись с тестовой информацией.'
                                 'Тестовая информация для тестовой записи',
                         'availability_status': 1}).json())

    if test_get:
        print(get(f'{link_website_2}api/developers_diary_admin/test@yandex.ru/test_123/10').json())

    if test_put:
        print(put(f'{link_website_2}api/developers_diary_admin/test@yandex.ru/test_123/10',
                  json={'availability_status': 0}).json())
        print(get(f'{link_website_2}api/developers_diary_admin/test@yandex.ru/test_123/10').json())

    if test_delete:
        print(delete(f'{link_website_2}api/developers_diary_admin/test@yandex.ru/test_123/10').json())
        print(get(f'{link_website_2}api/developers_diary_admin/test@yandex.ru/test_123/10').json())
