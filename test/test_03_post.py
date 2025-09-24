import pytest

@pytest.mark.parametrize('content,title,publish',[
                        ('This is test content 1','Title 1',True),
                        ('This is test content 2','Title 2',True),
                        ('This is test content 3','Title 3',True),
                        ('This is test content 4','Title 4',True),
                        ('This is test content 5','Title 5',True),

])
def test_post(client,access_token,content,title,publish):
    headers ={
        'Authorization': f"Bearer {access_token}"
    }
    response = client.post('/redditposts',headers=headers,json={'content':content,'title':title,'publish':publish})
    assert response.status_code == 201



def test_get_posts(client,access_token):
    headers ={
        'Authorization': f"Bearer {access_token}"
        }
    response = client.get('/redditposts',headers=headers)
    assert response.status_code == 200   
    assert len(response.json()) == 2


def test_get_posts_with_limit(client,access_token):
    headers ={
        'Authorization': f"Bearer {access_token}"
        }
    response = client.get('/redditposts?limit=10',headers=headers)
    assert response.status_code == 200   
    assert len(response.json()) > 2


@pytest.mark.parametrize('id',[1,2,3])
def test_get_post_with_id(client,access_token,id):
    headers ={
        'Authorization': f"Bearer {access_token}"
        }
    response = client.get(f'/redditposts/{id}',headers=headers)
    assert response.status_code == 200 


def test_vote_post(client,user,access_token):
    headers ={
        'Authorization': f"Bearer {access_token}"
    }
    response = client.get('/redditposts/votes',headers=headers)
#    print(f'{response.json()[0]["votes"]=}')
    assert response.status_code == 200

@pytest.mark.parametrize('id',[4,5])
def test_delete_post(client,access_token,id):
    headers ={
        'Authorization': f"Bearer {access_token}"
        }
    response = client.delete(f'/redditposts/{id}',headers=headers)
    assert response.status_code == 204
   
@pytest.mark.parametrize('id,content,title,publish',[
                        (1,'This is updated test content 1!','Title 1 updated',False),
                        (2,'This is updated test content 2!','Title 2 updated',False),
                        (3,'This is updated test content 3!','Title 3 updated',False),

])
def test_update_post(client,access_token,id,content,title,publish):
    headers ={
        'Authorization': f"Bearer {access_token}"
        }
    response = client.patch(f'/redditposts/{id}',headers=headers,json={'content':content,'title':title,'publish':publish})
#    print(response.json())
    assert response.status_code == 200



