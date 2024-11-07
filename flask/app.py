from flask import Flask, jsonify
from flasgger import Swagger
import csv
import os

# Criação da aplicação Flask
app = Flask(__name__)

# Configuração do Swagger
swagger = Swagger(app)

# Função para ler um arquivo CSV e retornar os dados
def read_csv(file_path):
    data = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                data.append(row)
    except Exception as e:
        return {"message": "Erro ao ler o arquivo.", "error": str(e)}
    return data

@app.route('/get_csv_data', methods=['GET'])
def get_csv_data():
    """
    Endpoint para obter dados dos arquivos CSV.
    ---
    tags:
      - CSV Data
    responses:
      200:
        description: Dados dos arquivos CSV
        content:
          application/json:
            schema:
              type: object
              properties:
                posts:
                  type: array
                  items:
                    type: array
                    example: ["id", "title", "content"]
                friendship:
                  type: array
                  items:
                    type: array
                    example: ["user1_id", "user2_id"]
                users:
                  type: array
                  items:
                    type: array
                    example: ["user_id", "user_name"]
    """
    # Caminhos dos arquivos CSV
    posts_path = 'posts.csv'
    friendship_path = 'friendship.csv'
    users_path = 'users.csv'
    
    # Verificar se os arquivos existem
    if not os.path.exists(posts_path) or not os.path.exists(friendship_path) or not os.path.exists(users_path):
        return jsonify({"message": "Um ou mais arquivos CSV não encontrados."}), 404
    
    # Ler os arquivos CSV
    posts_data = read_csv(posts_path)
    friendship_data = read_csv(friendship_path)
    users_data = read_csv(users_path)
    
    # Retornar os dados lidos dos arquivos CSV
    return jsonify({
        "posts": posts_data,
        "friendship": friendship_data,
        "users": users_data
    })

# Execução da aplicação Flask
if __name__ == "__main__":
    app.run(debug=True)
