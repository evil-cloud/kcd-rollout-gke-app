import pytest
from services.external_api import ExternalAPI

@pytest.fixture
def mock_external_api(mocker):
    return mocker.patch.object(ExternalAPI, "fetch_data", return_value={"mocked": "data"})

def test_external_api(mock_external_api):
    api = ExternalAPI()
    response = api.fetch_data()

    mock_external_api.assert_called_once() 
    
    assert response == {"mocked": "data"}