def test_user_login(user,client):
    response = client.post('/login', data={"username":'Mau@gmail.com','password':'password1234'})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_with_invalid_user(client):
    response = client.post('/login', data={"username":'Test@gmail.com','password':'password1234'})
    assert response.status_code == 401

def test_login_with_invalid_password(client):
    response = client.post('/login', data={"username":'Mau@gmail.com','password':'password'})
    assert response.status_code == 401
