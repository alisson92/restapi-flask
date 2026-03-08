import pytest
from unittest.mock import patch
from application import create_app


class TestApplication():

    @pytest.fixture
    def client(self):
        app = create_app('config.MockConfig')
        return app.test_client()

    def test_get_users(self, client):
        with patch('application.app.UserModel.objects') as mock_objects:
            mock_objects.return_value = []
            response = client.get('/users')
            assert response.status_code == 200
