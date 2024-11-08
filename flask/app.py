from flask import Flask, request, jsonify
from flask_restx import Api, Resource, reqparse
import os
from werkzeug.datastructures import FileStorage

# Criação da aplicação Flask
app = Flask(__name__)

# Configuração do Swagger
api = Api(app, doc="/swagger")
upload_parser = reqparse.RequestParser()
upload_parser.add_argument("file", type=FileStorage, location="files", required=True, help="Arquivo para upload")

@api.route("/uploadfile")
class FileUpload(Resource):
    @api.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        file = args["file"]

        if file.filename == "":
            return {"message": "Nenhum arquivo selecionado"}, 400

        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        try:
            file.save(file_path)
            return {"filename": file.filename, "message": "Arquivo enviado com sucesso"}, 200
        except Exception as e:
            return {"error": f"Erro ao salvar o arquivo {file.filename}: {str(e)}"}, 500
if __name__ == "__main__":
    app.run(debug=True)
