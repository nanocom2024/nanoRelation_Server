import pytest

def pytest_addoption(parser):
    parser.addoption('--baseurl', # オプション名
                    default='http://127.0.0.1:8181' # デフォルト値
                    )

@pytest.fixture
def baseurl(request):
    return request.config.getoption("--baseurl")