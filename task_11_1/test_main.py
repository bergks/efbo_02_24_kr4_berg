from fastapi.testclient import TestClient
import pytest
from main import app, cats_db

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def clean_db():
    cats_db.clear()
    yield

def test_create_cat_success(client):
    response = client.post('/cats',
                json={'name': 'Cat',
                    'age': 10,
                    'breed': 'breed1',
                    'color': 'black',
                    'vaccinated': True})
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == 'Cat'
    assert data['age'] == 10
    assert data['breed'] == 'breed1'
    assert data['vaccinated'] == True
    assert 'id' in data

def test_create_cat_invalid(client):
    response = client.post('/cats',
                           json={'name': 'Cat',
                                 'age': -10,
                                 'breed': 'breed1',
                                 'color': 'black',
                                 'vaccinated': True})
    assert response.status_code == 422

def test_get_cat_success(client):
    created = client.post('/cats',
                json={'name': 'Cat',
                    'age': 10,
                    'breed': 'breed1',
                    'color': 'black',
                    'vaccinated': True})
    cat_id = created.json()['id']

    response = client.get(f'/cats/{cat_id}')
    assert response.status_code == 200
    assert response.json()['name'] == 'Cat'

def test_get_cat_not_found(client):
    response = client.get('/cats/999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Cat not found'

def test_get_all_cats(client):
    response = client.get('/cats')
    assert response.status_code == 200

def test_delete_cat_success(client):
    created = client.post('/cats',
                          json={'name': 'Cat',
                                'age': 10,
                                'breed': 'breed1',
                                'color': 'black',
                                'vaccinated': True})
    cat_id = created.json()['id']

    response = client.delete(f'/cats/{cat_id}')
    assert response.status_code == 204

def test_delete_cat_not_found(client):
    response = client.delete('/cats/999')
    assert response.status_code == 404
    assert response.json()['detail'] == 'Cat not found'

def test_get_deleted_cat(client):
    created = client.post('/cats',
                          json={'name': 'Cat',
                                'age': 10,
                                'breed': 'breed1',
                                'color': 'black',
                                'vaccinated': True})
    cat_id = created.json()['id']

    client.delete(f'/cats/{cat_id}')

    response = client.get(f'/cats/{cat_id}')
    assert response.status_code == 404
