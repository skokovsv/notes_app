import pytest


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_note(client):
    response = await client.post(
        "/notes", json={"title": "Первая заметка", "content": "Тестовое содержимое"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Первая заметка"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_notes(client):
    await client.post("/notes", json={"title": "A", "content": "содержимое A"})
    await client.post("/notes", json={"title": "B", "content": "содержимое B"})

    response = await client.get("/notes")
    assert response.status_code == 200
    titles = [n["title"] for n in response.json()]
    assert "A" in titles and "B" in titles


@pytest.mark.asyncio
async def test_get_note_not_found(client):
    response = await client.get("/notes/does-not-exist")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_note(client):
    created = await client.post(
        "/notes", json={"title": "Удалю меня", "content": "..."}
    )
    note_id = created.json()["id"]

    delete_response = await client.delete(f"/notes/{note_id}")
    assert delete_response.status_code == 204

    get_response = await client.get(f"/notes/{note_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_create_note_validation_error(client):
    response = await client.post("/notes", json={"title": "", "content": ""})
    assert response.status_code == 422
