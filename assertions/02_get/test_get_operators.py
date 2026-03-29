def test_get_operators(get_operators_data):
    response = get_operators_data.get_operators()
    assert response.status_code == 200

    data = response.json()

    assert_get_operators(data) #вот как раз функция из файла assertions.py