from service.apiclient import APIClient
import csv
import os
from io import StringIO
from werkzeug.exceptions import BadRequest

class FileProcessor:
    """ Manager of files and folders processor."""

    def __init__(self):
        self.file_path = 'data/seu_file.csv'
        self.directory = 'data'
        self.api_client = APIClient()

    def upload_file_posts(self, file):
        """
        Upload a file to read and print data
        :param file: uploaded file
        :return: success or error
        """
        if file.filename.endswith('.csv'):
            try:
                contents = file.read().decode("utf-8")
                decoded_file = StringIO(contents)

                csv_reader = csv.DictReader(decoded_file)
                for row in csv_reader:
                    self.api_client.send_data(row)
                return {"mensagem": f"Arquivo {file.filename} processado com sucesso"}
            except Exception as e:
                raise BadRequest(f"Falha ao processar o arquivo CSV: {str(e)}")

        else:
            raise BadRequest("Apenas arquivo CSV")
        
    def upload_file_friendship(self, file):
        """
        Upload a file to read and print data
        :param file: uploaded file
        :return: success or error
        """
        if file.filename.endswith('.csv'):
            try:
                contents = file.read().decode("utf-8")
                decoded_file = StringIO(contents)

                csv_reader = csv.DictReader(decoded_file)
                for row in csv_reader:
                    self.api_client.send_data(row)
                return {"mensagem": f"Arquivo {file.filename} processado com sucesso"}
            except Exception as e:
                raise BadRequest(f"Falha ao processar o arquivo CSV: {str(e)}")

        else:
            raise BadRequest("Apenas arquivo CSV")    

    def upload_file_users(self, file):
        """
        Upload a file to read and print data
        :param file: uploaded file
        :return: success or error
        """
        if file.filename.endswith('.csv'):
            try:
                contents = file.read().decode("utf-8")
                decoded_file = StringIO(contents)

                csv_reader = csv.DictReader(decoded_file)
                for row in csv_reader:
                    self.api_client.send_data(row)
                return {"mensagem": f"Arquivo {file.filename} processado com sucesso"}
            except Exception as e:
                raise BadRequest(f"Falha ao processar o arquivo CSV: {str(e)}")

        else:
            raise BadRequest("Apenas arquivo CSV")        
              