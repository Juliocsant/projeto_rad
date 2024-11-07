from flask import Flask, jsonify
from flasgger import Swagger

# Criação da aplicação Flask
app = Flask(__name__)

# Configuração do Swagger
swagger = Swagger(app)

@app.route('/hello', methods=['GET'])
def hello_world():
    """
    Endpoint para retornar uma mensagem de olá.
    ---
    tags:
      - Hello
    responses:
      200:
        description: Mensagem de sucesso
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Hello, World!"
    """
    return jsonify({"message": "Hello, World!"})

# Execução da aplicação Flask
if __name__ == "__main__":
    app.run(debug=True)
