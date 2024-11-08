from service.apiclient import APIClient
import csv
import os
from io import StringIO
from werkzeug.exceptions import BadRequest

class FileProcessor:
    """ Manager of files and folders processor."""

    def __init__(self):
        self.api_client = APIClient()

    def upload_file_posts(self, file):
        try:
            # Verifica se o diretório de uploads existe, se não, cria
            if not os.path.exists("uploads"):
                os.makedirs("uploads")

            # Salva o arquivo no diretório de uploads
            file_path = os.path.join("uploads", file.filename)
            file.save(file_path)

            # Processa o arquivo CSV
            with open(file_path, mode='r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    print(row)  # Aqui você pode processar cada linha do CSV

            return {"message": f"Arquivo {file.filename} salvo e processado com sucesso"}, 200
        except Exception as e:
            return {"error": f"Erro ao salvar o arquivo {file.filename}: {str(e)}"}, 500

    def upload_file_friendship(self, file):
        try:
            # Verifica se o diretório de uploads existe, se não, cria
            if not os.path.exists("uploads"):
                os.makedirs("uploads")

            # Salva o arquivo no diretório de uploads
            file_path = os.path.join("uploads", file.filename)
            file.save(file_path)

            # Processa o arquivo CSV
            with open(file_path, mode='r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    print(row)  # Aqui você pode processar cada linha do CSV

            return {"message": f"Arquivo {file.filename} salvo e processado com sucesso"}, 200
        except Exception as e:
            return {"error": f"Erro ao salvar o arquivo {file.filename}: {str(e)}"}, 500

    def upload_file_users(self, file):
        """
        Upload a file to read and send data to the users endpoint
        :param file: uploaded file
        :return: success or error message
        """
        if file.filename.endswith('.csv'):
            try:
                contents = file.read().decode("utf-8")
                decoded_file = StringIO(contents)

                csv_reader = csv.DictReader(decoded_file)
                for row in csv_reader:
                    self.api_client.send_data_users(row)
                return {"mensagem": f"Arquivo {file.filename} processado com sucesso"}
            except Exception as e:
                raise BadRequest(f"Falha ao processar o arquivo CSV: {str(e)}")

        else:
            raise BadRequest("Apenas arquivo CSV")
