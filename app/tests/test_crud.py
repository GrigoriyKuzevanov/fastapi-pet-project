def test_create_and_get_author(test_client, post_author):
    response = test_client.post("/authors/", json=post_author)
    assert response.status_code == 200

    response = test_client.get(f"/authors/{1}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["fullname"] == "Test fullname"
    assert response_json["first_name"] == "Test first name"
    assert response_json["last_name"] == "Test last name"
    assert response_json["patronymic"] == "Test patronymic"
    assert response_json["birth_date"] == "1800-01-01"
    assert response_json["death_date"] == "1850-12-12"
