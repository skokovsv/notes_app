import pytest


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_note(client, auth_headers):
    response = await client.post(
        "/notes",
        json={"title": "Первая заметка", "content": "Тестовое содержимое"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Первая заметка"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_note_without_api_key_fails(client):
    response = await client.post(
        "/notes", json={"title": "Без ключа", "content": "..."}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_note_with_wrong_api_key_fails(client):
    response = await client.post(
        "/notes",
        json={"title": "Неверный ключ", "content": "..."},
        headers={"X-API-Key": "wrong-key"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_notes_is_public(client, auth_headers):
    await client.post("/notes", json={"title": "A", "content": "содержимое A"}, headers=auth_headers)
    await client.post("/notes", json={"title": "B", "content": "содержимое B"}, headers=auth_headers)

    response = await client.get("/notes")
    assert response.status_code == 200
    data = response.json()
    titles = [n["title"] for n in data["items"]]
    assert "A" in titles and "B" in titles
    assert data["total"] == 2


@pytest.mark.asyncio
async def test_list_notes_pagination(client, auth_headers):
    for i in range(15):
        await client.post("/notes", json={"title": f"Note {i}", "content": "..."}, headers=auth_headers)

    response = await client.get("/notes?page=1&page_size=10")
    data = response.json()
    assert len(data["items"]) == 10
    assert data["total"] == 15

    response_page2 = await client.get("/notes?page=2&page_size=10")
    data_page2 = response_page2.json()
    assert len(data_page2["items"]) == 5


@pytest.mark.asyncio
async def test_get_note_not_found(client):
    response = await client.get("/notes/does-not-exist")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_note(client, auth_headers):
    created = await client.post(
        "/notes", json={"title": "Удалю меня", "content": "..."}, headers=auth_headers
    )
    note_id = created.json()["id"]

    delete_response = await client.delete(f"/notes/{note_id}", headers=auth_headers)
    assert delete_response.status_code == 204

    get_response = await client.get(f"/notes/{note_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_note_without_api_key_fails(client, auth_headers):
    created = await client.post(
        "/notes", json={"title": "Не дам удалить", "content": "..."}, headers=auth_headers
    )
    note_id = created.json()["id"]

    delete_response = await client.delete(f"/notes/{note_id}")
    assert delete_response.status_code == 401


@pytest.mark.asyncio
async def test_create_note_validation_error(client, auth_headers):
    response = await client.post(
        "/notes", json={"title": "", "content": ""}, headers=auth_headers
    )
    assert response.status_code == 422