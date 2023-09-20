import requests


class AuthenticationService:
    def __init__(self, url):
        self.url = url

    def auth(self, email, password):
        try:
            req = requests.post(
                url=self.url,
                data={
                    'email': email,
                    'password': password
                }
            )
        except requests.exceptions.HTTPError as e:
            raise e

        return req.json().get('token')

    
