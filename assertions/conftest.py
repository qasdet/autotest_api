import os
import pytest
import allure
from dotenv import load_dotenv

from api_frame.create_operator import CreateOperatorAPI
from api_frame.get_countries import GetCountries
from api_frame.get_operators import GetOperatorsAPI
from dict_payload.payload_create_oper import localoperator, oper_praqe
from tools.get_country_id import get_country_ids

load_dotenv()


@pytest.fixture(scope='session')
def get_base_url():
    url = os.getenv('CLIENT')
    if not url:
        pytest.fail("CLIENT environment variable not set. Check your .env file.")
    return url


@pytest.fixture(scope='session')
def create_oper(get_base_url):
    return CreateOperatorAPI(get_base_url)


@pytest.fixture(scope='session')
def get_country(get_base_url):
    return GetCountries(get_base_url)


@pytest.fixture(scope='session')
def country_ids(get_country):
    return get_country_ids(get_country)


@pytest.fixture(scope='session')
def oper_local_payload(country_ids):
    return localoperator(country_ids)


@pytest.fixture(scope='session')
def oper_praqe_payload(country_ids):
    return oper_praqe(country_ids)


@pytest.fixture(scope='session')
def get_operators(get_base_url):
    return GetOperatorsAPI(get_base_url)


# Хуки Allure для добавления метаданных к отчетам
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        if hasattr(rep, "wasxfail"):
            return
        allure.attach(str(rep.longrepr), name="Error Details", attachment_type=allure.attachment_type.TEXT)