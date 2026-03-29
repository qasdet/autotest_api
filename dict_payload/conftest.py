import os
import pytest
from dotenv import load_dotenv

from api_frame.base_api import BaseAPI
from api_frame.create_operator import CreateOperatorAPI
from api_frame.get_countries import GetCountries
from tools.get_country_id import get_country_ids

load_dotenv()

@pytest.fixture(scope='session')
def base_api(get_base_url):
    return BaseAPI(get_base_url)

@pytest.fixture(scope='session')
def get_base_url():
    return os.getenv('CLIENT')

@pytest.fixture(scope='session')
def create_oper(get_base_url):
    return CreateOperatorAPI(get_base_url)

@pytest.fixture(scope='session')
def get_country(get_base_url):
    return GetCountries(get_base_url)

@pytest.fixture(scope='session')
def country_ids(get_country):
    return get_country_ids(get_country)