import requests

class BaseAPI():
    def __init__(self):
        self.base_url = base_url
        self.session = requests.Session()

    def _send_request(self,method,endpoint,**kwargs):
        url = f'{self.base_url}{endpoint}'
        try:
            response = self.session.request(method,url,**kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            print(f'HTTP error: {e.response.status_code} - {e.response.text}')
            raise

    def get_request(self,endpoint,**kwargs):
        return self._send_request('GET',endpoint,**kwargs)

    def post_request(self,endpoint,**kwargs):
        return self._send_request('POST',endpoint,**kwargs)

    def put_request(self,endpoint,**kwargs):
        return self._send_request('PUT',endpoint,**kwargs)