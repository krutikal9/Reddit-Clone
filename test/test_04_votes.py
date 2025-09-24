import pytest

@pytest.mark.parametrize('content,title,publish',[
                        ('This is test content 1','Title 1',True),
                        ('This is test content 2','Title 2',True),
                        ('This is test content 3','Title 3',True)

])
def test_vote_response(client,access_token,content,title,publish):
    headers ={
        'Authorization': f"Bearer {access_token}"
    }
    response = client.post('/redditposts',headers=headers,json={'content':content,'title':title,'publish':publish})
    # print(f'{response.json()["id"]=}')

    up_vote_response = client.post('/votes',headers=headers,json={'redditposts_id':response.json()["id"]})
    assert up_vote_response.json()['message'] =='Sucessfully added vote' 


    down_vote_response = client.post('/votes',headers=headers,json={'redditposts_id':response.json()["id"]})
    assert down_vote_response.json()['message'] =='Sucessfully removed vote'

