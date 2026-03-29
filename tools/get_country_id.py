def get_country_ids(get_country):
    rus_id = get_country.get_country_id('RUS'),
    kor_id = get_country.get_country_id('KOR')

    return {
        'rus_id' : rus_id,
        'kor_id' : kor_id
    }