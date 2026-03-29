from api_frame.base_api import BaseAPI
from api_frame.endpoints import POST_OPERATOR

class CreateOperatorAPI(BaseAPI):

    endpoint = POST_OPERATOR

    def create_operator(self,payload):
        response = self.post_request(endpoint=self.endpoint,json=payload)
        return response
    