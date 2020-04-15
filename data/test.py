from requests import get

test_version_first = True
if test_version_first:
    print(get('http://localhost:8000/api/get_publication/1').json())
    print(get('http://localhost:8000/api/get_publications').json())
