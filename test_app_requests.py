import requests
import json

BASE_URL = "http://127.0.0.1:5000"  # Адрес вашего Flask-сервера


# Тесты для маршрута '/api/country/<code>'

def test_get_country_by_alpha2():
    # Отправляем GET-запрос для получения страны по коду alpha2
    response = requests.get(f"{BASE_URL}/api/country/RU")  # Пример для России
    assert response.status_code == 200
    data = response.json()
    assert 'name' in data
    assert data['alpha2'] == 'RU'
    assert data['alpha3'] == 'RUS'
    assert data['region'] == 'Europe'  # Предположим, что регион России — Европа


def test_get_country_by_alpha3():
    # Отправляем GET-запрос для получения страны по коду alpha3
    response = requests.get(f"{BASE_URL}/api/country/RUS")  # Пример для России
    assert response.status_code == 200
    data = response.json()
    assert 'name' in data
    assert data['alpha3'] == 'RUS'
    assert data['alpha2'] == 'RU'
    assert data['region'] == 'Europe'


def test_get_country_not_found():
    # Отправляем GET-запрос для несуществующего кода
    response = requests.get(f"{BASE_URL}/api/country/XX")
    assert response.status_code == 404
    data = response.json()
    assert data['reason'] == 'Country not found'


def test_get_country_invalid_code():
    # Отправляем GET-запрос с недопустимым кодом
    response = requests.get(f"{BASE_URL}/api/country/INVALID")
    assert response.status_code == 400
    data = response.json()
    assert data['reason'] == 'Code is invalid'


# Тесты для маршрута '/api/user'

def test_create_user():
    # Создаем нового пользователя
    payload = {
        'username': 'testuser',
        'password': 'password123'
    }
    response = requests.post(f"{BASE_URL}/api/user", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert 'username' in data
    assert data['username'] == 'testuser'


def test_create_user_missing_fields():
    # Отправляем запрос с пустыми полями
    payload = {
        'username': '',
        'password': ''
    }
    response = requests.post(f"{BASE_URL}/api/user", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data['reason'] == 'Missing password or user name'


def test_create_user_already_exists():
    # Создание пользователя с уже существующим именем
    payload = {
        'username': 'existinguser',
        'password': 'password1234'
    }
    response = requests.post(f"{BASE_URL}/api/user", json=payload)

    # Попытка создать второго пользователя с тем же именем
    payload2 = {
        'username': 'existinguser',
        'password': 'newpassword'
    }
    response = requests.post(f"{BASE_URL}/api/user", json=payload2)

    assert response.status_code == 400
    data = response.json()
    assert data['reason'] == 'Username or password already exists'


def test_create_user_password_exists():
    # Создание пользователя с уже существующим паролем
    payload = {
        'username': 'user1',
        'password': 'password12345'
    }
    response = requests.post(f"{BASE_URL}/api/user", json=payload)

    # Попытка создать нового пользователя с таким же паролем
    payload2 = {
        'username': 'newuser',
        'password': 'password12345'
    }
    response = requests.post(f"{BASE_URL}/api/user", json=payload2)

    assert response.status_code == 400
    data = response.json()
    assert data['reason'] == 'Username or password already exists'


# Запуск всех тестов
if __name__ == '__main__':
    test_get_country_by_alpha2()
    test_get_country_by_alpha3()
    test_get_country_not_found()
    test_get_country_invalid_code()
    test_create_user()
    test_create_user_missing_fields()
    test_create_user_already_exists()
    test_create_user_password_exists()

    print("Все тесты прошли успешно!")