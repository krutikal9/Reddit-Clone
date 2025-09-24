import pytest

def test_no_user(client):
    response =client.get('/users')
    print(response.json())
    assert response.json() == []
    assert response.status_code ==200



@pytest.mark.parametrize('email, password',
                         [
                            ('test@gmail.com','password1234'),
                            ('test1@gmail.com','password1234'),
                            ('test2@gmail.com','password1234')

                         ])
def test_create_user(client,email,password):
    response =client.post('/users',json={"email":email, "password": password})
    print(response.json())
    assert response.status_code ==201


@pytest.mark.parametrize('id',[1,2,3])
def test_get_user_with_id(client,id):
    response = client.get(f'users/{id}')
    print(response.json())
    assert response.status_code ==200


@pytest.mark.parametrize('id',[4,5,6])
def test_get_user_with_invalid_id(client,id):
    response = client.get(f'users/{id}')
    print(response.json())
    assert response.status_code ==404


