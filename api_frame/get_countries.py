from api_frame.base_api import BaseAPI
from api_frame.endpoints import GET_COUNTRY

class GetCountries(BaseAPI):
    endpoint = GET_COUNTRY

    def get_countries(self):
        response=self.get_request(self.endpoint)
        return response

    def get_country_id(self,country_code):
        response = self.get_request(self.endpoint)
        data = response.json()
        items = data['items']

        for item in items:
            if item['countryCode'] == country_code:
                return item['countryId']
        return None