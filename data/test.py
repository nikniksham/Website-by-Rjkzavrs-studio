from requests import get, post, delete, put

test_user_version_first = True
test_user_version_second = False
test_version_second = False
test_version_third = False

link_website = 'https://rjkzavrs-studio.herokuapp.com/'
link_website_2 = 'http://localhost:8000/'
test_get = False
test_post = False
test_delete = False
test_put = True
if test_user_version_first:
    if test_post:
        print(get(f'{link_website_2}api/user/test_account@yandex.ru/test_123').json())
        print(post(f'{link_website_2}api/user',
                   json={'id': 10,
                         'name': 'Николай',
                         'surname': 'Шамков',
                         'age': 16,
                         'nickname': 'nikniksham',
                         'email': 'test_account@yandex.ru',
                         'password': 'test_123'}).json())

    if test_get:
        print(get(f'{link_website_2}api/user/test_account@yandex.ru/test_123').json())

    if test_put:
        print(put(f'{link_website_2}api/user/test_account@yandex.ru/test_123', json={'agggfbe': 20}).json())
        # print(get(f'{link_website_2}api/user/test_account@yandex.ru/test_123').json())

    if test_delete:
        print(delete(f'{link_website_2}api/user/test_account@yandex.ru/test_123').json())
        print(get(f'{link_website_2}api/user/test_account@yandex.ru/test_123').json())

if test_version_second:
    if test_post:
        print(get(f'{link_website_2}api/developers_diary_admin/test@yandex.ru/test_123/10').json())
        print(post(f'{link_website_2}api/developers_diary_admin_create/test@yandex.ru/test_123',
                   json={'id': 10,
                         'header': 'Тестовая запись 2',
                         'body': 'Тестовая запись с тестовой информацией.'
                                 'Тестовая информация для тестовой записи',
                         'availability_status': 1}).json())

    if test_get:
        print(get(f'{link_website_2}api/developers_diary_admin/test@yandex.ru/test_123/10').json())

    if test_put:
        print(put(f'{link_website_2}api/developers_diary_admin/test@yandex.ru/test_123/10',
                  json={'availability_status': 0}).json())
        # print(get(f'{link_website_2}api/developers_diary_admin/test@yandex.ru/test_123/10').json())

    if test_delete:
        print(delete(f'{link_website_2}api/developers_diary_admin/test@yandex.ru/test_123/10').json())
        print(get(f'{link_website_2}api/developers_diary_admin/test@yandex.ru/test_123/10').json())


if test_version_third:
    if test_post:
        print(get(f'{link_website_2}api/publication/test@yandex.ru/test_123/10').json())
        print(post(f'{link_website_2}api/publication_create/test@yandex.ru/test_123',
                   json={'id': 10,
                         'header': 'Тестовая запись',
                         'body': 'Тестовая запись с тестовой информацией.'
                                 'Тестовая информация для тестовой записи'}).json())

    if test_get:
        print(get(f'{link_website_2}api/publication/test@yandex.ru/test_123/10').json())

    if test_put:
        print(put(f'{link_website_2}api/publication/test@yandex.ru/test_123/10',
                  json={'header': 'Тестовая смена загаловка'}).json())
        print(get(f'{link_website_2}api/publication/test@yandex.ru/test_123/10').json())

    if test_delete:
        print(delete(f'{link_website_2}api/publication/test@yandex.ru/test_123/10').json())
        print(get(f'{link_website_2}api/publication/test@yandex.ru/test_123/10').json())


a, b = False, False
if a:
    for i in range(1, 101):
        print(post(f'{link_website_2}api/developers_diary_admin_create/test@yandex.ru/test_123',
                   json={'id': i,
                         'header': f'Тестовая запись_{i}',
                         'body': 'Тестовая запись с тестовой информацией.'
                                 'Тестовая информация для тестовой записи',
                         'availability_status': 1}).json())
if b:
    for i in range(1, 163):
        print(delete(f'{link_website_2}api/developers_diary_admin/test@yandex.ru/test_123/{i}').json())
