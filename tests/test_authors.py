def test_create_and_get_author(test_client, post_author):
    # create user with id=1
    response = test_client.post("/authors/", json=post_author)
    assert response.status_code == 200

    # get user with id=1
    response = test_client.get(f"/authors/{1}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["fullname"] == "Test fullname"
    assert response_json["first_name"] == "Test first name"
    assert response_json["last_name"] == "Test last name"
    assert response_json["patronymic"] == "Test patronymic"
    assert response_json["birth_date"] == "1800-01-01"
    assert response_json["death_date"] == "1850-12-12"


def test_create_and_update_author(test_client, post_author, update_author):
    # create user with id=1
    response = test_client.post("/authors/", json=post_author)
    assert response.status_code == 200

    # update user with id=1
    response = test_client.put(f"/authors/{1}", json=update_author)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["fullname"] == "Test update fullname"
    assert response_json["first_name"] == "Test update first name"
    assert response_json["last_name"] == "Test update last name"
    assert response_json["patronymic"] == "Test update patronymic"
    assert response_json["birth_date"] == "1900-01-01"
    assert response_json["death_date"] == "1950-12-12"


def test_create_and_patch_author(test_client, post_author, partically_update_author):
    # create user with id=1
    response = test_client.post("/authors/", json=post_author)
    assert response.status_code == 200

    # patch update user with id=1
    response = test_client.patch(f"/authors/{1}", json=partically_update_author)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["fullname"] == "Test patch fullname"
    assert response_json["first_name"] == "Test first name"
    assert response_json["last_name"] == "Test last name"
    assert response_json["patronymic"] == "Test patronymic"
    assert response_json["birth_date"] == "1700-01-01"
    assert response_json["death_date"] == "1850-12-12"


def test_create_and_delete_author(test_client, post_author):
    # create user with id=1
    response = test_client.post("/authors/", json=post_author)
    assert response.status_code == 200
    response = test_client.get("/authors")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # delete user with id=1
    response = test_client.delete(f"/authors/{1}")
    assert response.status_code == 200
    response = test_client.get("/authors")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_get_author_not_found(test_client):
    response = test_client.get("/authors/100")
    assert response.status_code == 404
    response_json = response.json()
    assert response_json["detail"] == "Author with id: 100 is not found"
