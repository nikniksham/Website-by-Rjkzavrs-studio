from requests import get, post, delete, put

test_user_version_first = False
test_user_version_second = False
test_developers_diary_version_first = True
test_publication_version_first = True
test_publication_version_second = True

link_website = 'https://rjkzavrs-studio.herokuapp.com/'
link_website_2 = 'http://localhost:8000/'
test_get = True
test_post = True
test_delete = True
test_put = True
if test_user_version_first:
    if test_post:
        print(get(f'{link_website_2}api/user/test_account@yandex.ru/test_123').json())
        print(post(f'{link_website_2}api/user',
                   json={'id': 100,
                         'name': 'Николай',
                         'surname': 'Шамков',
                         'age': 16,
                         'nickname': 'nikniksham',
                         'email': 'test_account@yandex.ru',
                         'password': 'test_123'}).json())

    if test_get:
        print(get(f'{link_website_2}api/user/test_account@yandex.ru/test_123').json())

    if test_put:
        print(put(f'{link_website_2}api/user/test_account@yandex.ru/test_123', json={'age': 20}).json())
        print(get(f'{link_website_2}api/user/test_account@yandex.ru/test_123').json())

    if test_delete:
        print(delete(f'{link_website_2}api/user/test_account@yandex.ru/test_123').json())
        print(get(f'{link_website_2}api/user/test_account@yandex.ru/test_123').json())

if test_user_version_second:
    if test_get:
        print(get(f'{link_website_2}api/user/test@yandex.ru/test_123/9').json())
        print(get(f'{link_website_2}api/users/test@yandex.ru/test_123').json())

    if test_put:
        print(put(f'{link_website_2}api/user/test@yandex.ru/test_123/9', json={'age': 15}).json())
        print(get(f'{link_website_2}api/user/test@yandex.ru/test_123/9').json())

    if test_delete:
        print(delete(f'{link_website_2}api/user/test@yandex.ru/test_123/9').json())
        print(get(f'{link_website_2}api/user/test@yandex.ru/test_123/9').json())


if test_developers_diary_version_first:
    if test_post:
        print(get(f'{link_website_2}api/developers_diary_admin/test@yandex.ru/test_123/100').json())
        print(post(f'{link_website_2}api/developers_diary_admin_create/test@yandex.ru/test_123',
                   json={'id': 100,
                         'header': 'Тестовая запись 2',
                         'body': 'Тестовая запись с тестовой информацией.'
                                 'Тестовая информация для тестовой записи',
                         'availability_status': 2}).json())

    if test_get:
        print(get(f'{link_website_2}api/developers_diary_admin_list/test@yandex.ru/test_123').json())
        print(get(f'{link_website_2}api/developers_diary_admin/test@yandex.ru/test_123/100').json())

    if test_put:
        print(put(f'{link_website_2}api/developers_diary_admin/test@yandex.ru/test_123/100',
                  json={'header': 'Тестовая смена названия 1'}).json())
        print(get(f'{link_website_2}api/developers_diary_admin/test@yandex.ru/test_123/100').json())

    if test_delete:
        print(delete(f'{link_website_2}api/developers_diary_admin/test@yandex.ru/test_123/100').json())
        print(get(f'{link_website_2}api/developers_diary_admin/test@yandex.ru/test_123/100').json())


if test_publication_version_first:
    if test_post:
        print(get(f'{link_website_2}api/publication/test_account2@yandex.ru/test_123/100').json())
        print(post(f'{link_website_2}api/publication_create/test_account2@yandex.ru/test_123',
                   json={'id': 100,
                         'header': 'Тестовая запись',
                         'body': 'Тестовая запись с тестовой информацией.'
                                 'Тестовая информация для тестовой записи'}).json())

    if test_get:
        print(get(f'{link_website_2}api/publication/test_account2@yandex.ru/test_123/100').json())

    if test_put:
        print(put(f'{link_website_2}api/publication/test_account2@yandex.ru/test_123/100',
                  json={'header': 'Тестовая смена загаловка'}).json())
        print(get(f'{link_website_2}api/publication/test_account2@yandex.ru/test_123/100').json())

    if test_delete:
        print(delete(f'{link_website_2}api/publication/test_account2@yandex.ru/test_123/100').json())
        print(get(f'{link_website_2}api/publication/test_account2@yandex.ru/test_123/100').json())


if test_publication_version_second:
    if test_post:
        print(get(f'{link_website_2}api/publication/test@yandex.ru/test_123/100').json())
        print(post(f'{link_website_2}api/publication_create/test@yandex.ru/test_123',
                   json={'id': 100,
                         'header': 'Тестовая запись',
                         'body': 'Тестовая запись с тестовой информацией.'
                                 'Тестовая информация для тестовой записи'}).json())

    if test_get:
        print(get(f'{link_website_2}api/publication/test@yandex.ru/test_123/100').json())

    if test_put:
        print(put(f'{link_website_2}api/publication/test@yandex.ru/test_123/100',
                  json={'header': 'Тестовая смена загаловка'}).json())
        print(get(f'{link_website_2}api/publication/test@yandex.ru/test_123/100').json())

    if test_delete:
        print(delete(f'{link_website_2}api/publication/test@yandex.ru/test_123/100').json())
        print(get(f'{link_website_2}api/publication/test@yandex.ru/test_123/100').json())
