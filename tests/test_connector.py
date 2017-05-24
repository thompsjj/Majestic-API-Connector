import majestic_api.APIService as APIService

majestic_test_url = 'http://developer.majestic.com/api_command'
majestic_api_key = 'Your Key Goes Here'


def test_connector():
    payload = {'Mode': '0', 'Count': '10', 'item': 'http://www.majestic.com', 'datasource': 'fresh'}
    api_service = APIService.APIService(majestic_api_key, majestic_test_url)
    response = api_service.execute_command('GetIndexItemInfo', payload)
    assert response.is_ok() is True

