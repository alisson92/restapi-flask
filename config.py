import os


class DevConfig():

    MONGODB_SETTINGS = {
        'db': os.getenv('MONGO_DB'),
        'host': os.getenv('MONGO_HOST'),
        'username': os.getenv('MONGO_USERNAME'),
        'password': os.getenv('MONGO_PASSWORD')
    }


class ProdConfig():

    MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
    MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')
    MONGODB_HOST = os.getenv('MONGODB_HOST')
    MONGODB_DB = os.getenv('MONGODB_DB')

    MONGODB_SETTINGS = {
        'host': 'mongodb+srv://%s:%s@%s/%s?appName=Cluster0' % (
            MONGODB_USERNAME,
            MONGODB_PASSWORD,
            MONGODB_HOST,
            MONGODB_DB
        )
    }


class MockConfig():

    MONGODB_SETTINGS = {
        'db': 'users',
        'host': 'mongodb://localhost',
    }
