from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_mongoengine import MongoEngine
from mongoengine import NotUniqueError
import re

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'users',
    'host': 'mongodb',
    'port': 27017,
    'username': 'admin',
    'password': 'admin'
}

parser = reqparse.RequestParser()
parser.add_argument('first_name',
                    type=str,
                    required=True,
                    help="First name is required"
                    )
parser.add_argument('last_name',
                    type=str,
                    required=True,
                    help="Last name is required"
                    )
parser.add_argument('cpf',
                    type=str,
                    required=True,
                    help="CPF is required"
                    )
parser.add_argument('email',
                    type=str,
                    required=True,
                    help="Email is required"
                    )
parser.add_argument('birth_date',
                    type=str,
                    required=True,
                    help="Birth date is required"
                    )


api = Api(app)
db = MongoEngine(app)


class UserModel(db.Document):
    cpf = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True)
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    birth_date = db.DateField(required=True)


class Users(Resource):
    def get(self):
        return {"message": "user 1"}


class User(Resource):

    def validate_cpf(self, cpf: str) -> bool:

        # 1. Remove formatting (keep only numbers)
        cpf = re.sub(r'[^0-9]', '', cpf)

        # 2. Check length and invalid repeated numbers (e.g., 111.111.111-11)
        if len(cpf) != 11 or len(set(cpf)) == 1:
            return False

        # 3. Algorithm: Validate first digit (9th digit + 1st check digit)
        sum_1 = 0
        for i in range(9):
            sum_1 += int(cpf[i]) * (10 - i)

        first_digit = (sum_1 * 10 % 11)
        if first_digit == 10:
            first_digit = 0

        if int(cpf[9]) != first_digit:
            return False

        # 4. Algorithm: Validate second digit (10th digit + 2nd check digit)
        sum_2 = 0
        for i in range(10):
            sum_2 += int(cpf[i]) * (11 - i)

        second_digit = (sum_2 * 10 % 11)
        if second_digit == 10:
            second_digit = 0

        if int(cpf[10]) != second_digit:
            return False

        return True

    def post(self):
        data = parser.parse_args()

        if not self.validate_cpf(data["cpf"]):
            return {"message": "Invalid CPF!"}, 400

        try:
            response = UserModel(**data).save()
            return {"message": "User %s created successfully!" % response.id}
        except NotUniqueError:
            return {"message": "CPF already exists in database!"}, 400
        
    def get(self):
        return {"message": "CPF"}


api.add_resource(Users, '/users')
api.add_resource(User, '/user', '/user/<string:cpf>')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
