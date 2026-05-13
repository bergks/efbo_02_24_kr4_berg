import pytest
from httpx import AsyncClient, ASGITransport
from faker import Faker

from main import app, cats_db

fake = Faker()

@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.fixture(autouse=True)
def clean_db():
    cats_db.clear()
    yield

@pytest.mark.asyncio
async def test_create_cat_success(client):
    cat_data = {
        'name': fake.first_name(),
        'age': fake.random_int(min=0),
        'breed': fake.word(),
        'color': fake.color_name(),
        'vaccinated': fake.boolean()
    }

    response = await client.post('/cats', json = cat_data)
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == cat_data['name']
    assert data['age'] == cat_data['age']
    assert data['color'] == cat_data['color']
    assert data['breed'] == cat_data['breed']
    assert data['vaccinated'] == cat_data['vaccinated']
    assert 'id' in data

@pytest.mark.asyncio
async def test_create_cat_invalid(client):
    response = await client.post("/cats", json={"name": fake.name()})  # нет age
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_user_success(client):
    cat_data = {
        'name': fake.first_name(),
        'age': fake.random_int(min=0),
        'breed': fake.word(),
        'color': fake.color_name(),
        'vaccinated': fake.boolean()
    }
    create_resp = await client.post("/cats", json=cat_data)
    cat_id = create_resp.json()["id"]

    response = await client.get(f"/cats/{cat_id}")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_cat_not_found(client):
    response = await client.get("/cats/not-a-real-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cat not found"


@pytest.mark.asyncio
async def test_delete_cat_success(client):
    cat_data = {
        'name': fake.first_name(),
        'age': fake.random_int(min=0),
        'breed': fake.word(),
        'color': fake.color_name(),
        'vaccinated': fake.boolean()
    }
    create_resp = await client.post("/cats", json=cat_data)
    cat_id = create_resp.json()["id"]

    response = await client.delete(f"/cats/{cat_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_cat_twice(client):
    cat_data = {
        'name': fake.first_name(),
        'age': fake.random_int(min=0),
        'breed': fake.word(),
        'color': fake.color_name(),
        'vaccinated': fake.boolean()
    }

    create_resp = await client.post("/cats", json=cat_data)
    cat_id = create_resp.json()["id"]

    await client.delete(f"/cats/{cat_id}")

    response = await client.delete(f"/cats/{cat_id}")  # второе — 404
    assert response.status_code == 404