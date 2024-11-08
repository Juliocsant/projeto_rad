import requests

class APIClient:
    def __init__(self):
        self.api_url_posts = "http://127.0.0.1:8000/posts/"
        self.api_url_posts = "http://127.0.0.1:8000/posts/"


    def send_data(self, data):
        try:
            response = requests.post(self.api_url, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao enviar dados: {e}")
        