import pytest
from unittest.mock import patch
from application import create_app


class TestApplication():

    @pytest.fixture
    def client(self):
        app = create_app('config.MockConfig')
        return app.test_client()

    @pytest.fixture
    def valid_user(self):
        return {
            "first_name": "Alisson",
            "last_name": "Lima",
            "cpf": "482.708.180-89",
            "email": "alisson.lima@test.com.br",
            "birth_date": "1992-03-10"
            }

    @pytest.fixture
    def invalid_user(self):
        return {
            "first_name": "Alisson",
            "last_name": "Lima",
            "cpf": "482.708.180-88",
            "email": "alisson.lima@test.com.br",
            "birth_date": "1992-03-10"
            }

    def test_get_users(self, client):
        with patch('application.app.UserModel.objects') as mock_objects:
            mock_objects.return_value = []
            response = client.get('/users')
            assert response.status_code == 200

    def test_post_user(self, client, valid_user, invalid_user):
        with patch('application.app.UserModel.save') as mock_save:
            mock_save.return_value.id = "mock_id_123"
            response = client.post('/user', json=valid_user)
            assert response.status_code == 200
            assert b"successfull" in response.data

            response = client.post('/user', json=invalid_user)
            assert response.status_code == 400
            assert b"Invalid" in response.data

    def test_get_user(self, client, valid_user, invalid_user):
        with patch('application.app.UserModel.objects') as mock_objects:
            mock_objects.return_value = [valid_user]
            response = client.get('/user/%s' % valid_user["cpf"])
            assert response.status_code == 200
            assert response.json[0]["first_name"] == "Alisson"
            assert response.json[0]["last_name"] == "Lima"
            assert response.json[0]["cpf"] == "482.708.180-89"
            assert response.json[0]["email"] == "alisson.lima@test.com.br"
            assert response.json[0]["birth_date"] == "1992-03-10"

            mock_objects.return_value = []
            response = client.get('/user/%s' % invalid_user["cpf"])
            assert response.status_code == 404
            assert b"User not found!" in response.data
