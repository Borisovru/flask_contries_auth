from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cd_collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Модели
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contryCode = db.Column(db.String(2), nullable=False)
    isPublic = db.Column(db.Boolean, nullable=False, default=False)
    phoneNumber = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(120), nullable=False)

class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    alpha2 = db.Column(db.String(2), unique=True, nullable=False)
    alpha3 = db.Column(db.String(3), unique=True, nullable=False)
    region = db.Column(db.String(80))

# Функции для преобразования в JSON
def present_country(country):
    return {
        'name': country.name,
        'alpha2': country.alpha2,
        'alpha3': country.alpha3,
        'region': country.region
    }

def present_user(user):
    return {
        'username': user.username,
        'password': user.password,
        'email': user.email,
        'contryCode': user.contryCode,
        'phoneNumber': user.phoneNumber,
        'image': user.image,
        'isPublic': user.isPublic,
    }

# Маршрут для получения информации о стране
@app.route('/api/country/<code>', methods=['GET'])
def get_country(code):
    if len(code) == 2:
        country = Country.query.filter_by(alpha2=code).first()
        if not country:
            return jsonify({'reason': 'Country not found'}), 404
        return jsonify(present_country(country))
    elif len(code) == 3:
        country = Country.query.filter_by(alpha3=code).first()
        if not country:
            return jsonify({'reason': 'Country not found'}), 404
        return jsonify(present_country(country))
    else:
        return jsonify({'reason': 'Code is invalid'}), 400

# Маршрут для создания пользователя
@app.route('/api/user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()  # Получаем данные из запроса
        if not data:
            return jsonify({'reason': 'Invalid JSON data'}), 400  # Если JSON пустой

        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        countryCode = data.get('countryCode')
        isPublic = data.get('isPublic')
        phoneNumber = data.get('phoneNumber')
        image = data.get('image')


        # Проверка на пустые поля
        if not username or not password:
            return jsonify({'reason': 'Missing password or user name'}), 400

        # Проверка на уникальность имени и пароля
        if User.query.filter_by(username=username).first() is not None or User.query.filter_by(password=password).first() is not None or User.query.filter_by(email=email).first() is not None:
            return jsonify({'reason': 'Username, password or email already exists'}), 400

        # Создание нового пользователя
        user = User(username=username, password=password, email=email, countryCode=countryCode, isPublic=isPublic, phoneNumber=phoneNumber, image=image)
        db.session.add(user)
        db.session.commit()  # Сохраняем изменения в базе данных

        return jsonify(present_user(user)), 200  # Возвращаем данные о созданном пользователе

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'reason': 'Server error'}), 500  # Обработка ошибок

if __name__ == '__main__':
    app.run(debug=True)
