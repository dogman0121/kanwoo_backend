def test_create_collection(
    authorized_client, 
    csrf_access_token,
    privacy_id
):
    collection_name = "test"
    collection_privacy_id = privacy_id

    response = authorized_client.post(
        "/v1/collections", 
        headers={
            "X-CSRF-TOKEN": csrf_access_token
        },
        json={
            "name": collection_name,
            "privacy": collection_privacy_id
        }
    )

    print(response.json)
    assert response.status_code == 201
