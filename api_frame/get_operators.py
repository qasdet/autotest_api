from api_frame.base_api import BaseAPI
from api_frame.endpoints import GET_OPERATOR

class GetOperatorsAPI(BaseAPI):

    endpoint = GET_OPERATOR

    def get_operators(self):
        response = self.get_request(endpoint=self.endpoint)
        return response.json()