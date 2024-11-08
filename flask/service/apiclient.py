import requests

class APIClient:
    def __init__(self):
        self.api_url_posts = "http://127.0.0.1:8000/uploadfile/posts"
        self.api_url_friendship = "http://127.0.0.1:8000/uploadfile/friendship"
        self.api_url_users = "http://127.0.0.1:8000/uploadfile/users"

    def send_data_posts(self, data):
        try:
            response = requests.post(self.api_url_posts, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao enviar dados para posts: {e}")

    def send_data_friendship(self, data):
        try:
            response = requests.post(self.api_url_friendship, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao enviar dados para friendship: {e}")

    def send_data_users(self, data):
        try:
            response = requests.post(self.api_url_users, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao enviar dados para users: {e}")