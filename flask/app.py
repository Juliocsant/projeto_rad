from flask import Flask, request, jsonify
from flask_restx import Api, Resource, reqparse
import os
from werkzeug.datastructures import FileStorage
from controller.file_processor import FileProcessor

# Criação da aplicação Flask
app = Flask(__name__)

# Configuração do Swagger
api = Api(app, doc="/swagger")
upload_parser = reqparse.RequestParser()
upload_parser.add_argument("file", type=FileStorage, location="files", required=True, help="Arquivo para upload")

@api.route("/uploadfile/posts")
class FileUploadPosts(Resource):
    @api.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        file = args["file"]

        if file.filename == "":
            return {"message": "Nenhum arquivo selecionado"}, 400

        read_file = FileProcessor()

        try:
            return read_file.upload_file_posts(file)
        except Exception as e:
            return {"error": f"Erro ao salvar o arquivo {file.filename}: {str(e)}"}, 500
        
@api.route("/uploadfile/frienship")
class FileUploadFriendship(Resource):
    @api.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        file = args["file"]

        if file.filename == "":
            return {"message": "Nenhum arquivo selecionado"}, 400

        read_file = FileProcessor()

        try:
            return read_file.upload_file_frienship(file)
        except Exception as e:
            return {"error": f"Erro ao salvar o arquivo {file.filename}: {str(e)}"}, 500

@api.route("/uploadfile/users")
class FileUploadUsers(Resource):
    @api.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        file = args["file"]

        if file.filename == "":
            return {"message": "Nenhum arquivo selecionado"}, 400

        read_file = FileProcessor()

        try:
            return read_file.upload_file_users(file)
        except Exception as e:
            return {"error": f"Erro ao salvar o arquivo {file.filename}: {str(e)}"}, 500

if __name__ == "__main__":
    app.run(debug=True)
