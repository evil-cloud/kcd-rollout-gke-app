import pytest
from services.business_logic import process_data
from services.external_api import ExternalAPI

@pytest.fixture
def mock_external_api(mocker):
    return mocker.patch.object(ExternalAPI, "fetch_data", return_value={"info": "ok"})

def test_process_data(mock_external_api):
    result = process_data()

    # Se asegura de que el mensaje contenga la estructura esperada
    assert result == {"message": "Datos procesados correctamente: {'info': 'ok'}"}