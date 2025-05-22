from services.external_api import ExternalAPI

def process_data():
    api = ExternalAPI()
    external_data = api.fetch_data()
    return {"message": f"Datos procesados correctamente: {external_data}"}