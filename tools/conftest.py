import os
import pytest
from dotenv import load_dotenv

from api_frame.get_countries import GetCountries
from api_frame.base_api import BaseAPI

load_dotenv()


@pytest.fixture(scope='session')
def get_base_url():
    return os.getenv('CLIENT')

@pytest.fixture(scope='session')
def base_api(get_base_url):
    return BaseAPI(get_base_url)

@pytest.fixture(scope='session')
def get_country(get_base_url):
    return GetCountries(get_base_url)