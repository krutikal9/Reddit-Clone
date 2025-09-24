import pytest 
from app.config import settings
from sqlmodel import Field, Session, SQLModel, create_engine
from app.main import app
from app.database import get_db
from fastapi.testclient import TestClient


@pytest.fixture(scope='module', autouse=True)
def setup_teardown():
    DB_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'
    engine = create_engine(DB_URL)
    def get_test_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_db] = get_test_session
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(scope='module')
def client():
    return TestClient(app)

@pytest.fixture(scope='module')
def user(client):
    test_user = client.post('/users',json={'email':'Mau@gmail.com', 'password':'password1234'})
    return test_user


@pytest.fixture(scope='module')
def access_token(client,user):
    test_login = client.post('/login', data= {'username':'Mau@gmail.com','password':'password1234'})
    return test_login.json()['access_token']


