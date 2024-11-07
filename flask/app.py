from flask import Flask, jsonify, request
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

# Função para escrever dados em um arquivo CSV
def write_csv(file_path, data):
    try:
        with open(file_path, mode='w', encoding='utf-8', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(data)
    except Exception as e:
        return {"message": "Erro ao escrever no arquivo.", "error": str(e)}
    return {"message": "Dados escritos com sucesso."}

# Endpoint para importar dados dos arquivos CSV
@app.route('/importar-usuarios/', methods=['POST'])
def importar_usuarios():
    """
    Endpoint para importar dados dos usuários.
    ---
    tags:
      - Importação de Dados
    responses:
      200:
        description: Dados dos usuários importados com sucesso
    """
    users_data = read_csv('users.csv')
    # Aqui você pode validar e salvar os dados no banco de dados, se necessário.
    return jsonify({"message": "Usuários importados com sucesso", "data": users_data})

@app.route('/importar-amigos/', methods=['POST'])
def importar_amigos():
    """
    Endpoint para importar dados das amizades.
    ---
    tags:
      - Importação de Dados
    responses:
      200:
        description: Dados das amizades importados com sucesso
    """
    friendship_data = read_csv('friendship.csv')
    # Validação e armazenamento no banco de dados
    return jsonify({"message": "Amigos importados com sucesso", "data": friendship_data})

@app.route('/importar-postagens/', methods=['POST'])
def importar_postagens():
    """
    Endpoint para importar dados das postagens.
    ---
    tags:
      - Importação de Dados
    responses:
      200:
        description: Dados das postagens importados com sucesso
    """
    posts_data = read_csv('posts.csv')
    # Validação e armazenamento no banco de dados
    return jsonify({"message": "Postagens importadas com sucesso", "data": posts_data})

# Endpoint para gerenciar usuários (Cadastro, Edição, Exclusão)
@app.route('/usuarios/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gerenciar_usuarios():
    """
    Gerenciar usuários (Cadastro, Edição, Exclusão)
    ---
    tags:
      - Usuários
    responses:
      200:
        description: Operação realizada com sucesso
    """
    if request.method == 'GET':
        users_data = read_csv('users.csv')
        return jsonify({"users": users_data})

    elif request.method == 'POST':
        # Cadastrar um novo usuário
        new_user = request.json
        users_data = read_csv('users.csv')
        users_data.append([new_user['id'], new_user['nome'], new_user['email'], new_user['data_nascimento']])
        write_csv('users.csv', users_data)
        return jsonify({"message": "Usuário cadastrado com sucesso", "user": new_user}), 201

    elif request.method == 'PUT':
        # Editar um usuário existente
        updated_user = request.json
        users_data = read_csv('users.csv')
        for user in users_data:
            if user[0] == updated_user['id']:
                user[1] = updated_user['nome']
                user[2] = updated_user['email']
                user[3] = updated_user['data_nascimento']
                break
        write_csv('users.csv', users_data)
        return jsonify({"message": "Usuário atualizado com sucesso", "user": updated_user})

    elif request.method == 'DELETE':
        # Excluir um usuário
        user_id = request.args.get('id')
        users_data = read_csv('users.csv')
        users_data = [user for user in users_data if user[0] != user_id]
        write_csv('users.csv', users_data)
        return jsonify({"message": "Usuário excluído com sucesso"})


# Endpoint para gerenciar amizades (Adicionar, Remover, Bloquear)
@app.route('/amigos/', methods=['POST', 'DELETE'])
def gerenciar_amigos():
    """
    Gerenciar amizades (Adicionar, Remover, Bloquear)
    ---
    tags:
      - Amigos
    responses:
      200:
        description: Operação realizada com sucesso
    """
    if request.method == 'POST':
        new_friendship = request.json
        friendship_data = read_csv('friendship.csv')
        friendship_data.append([new_friendship['user1_id'], new_friendship['user2_id'], new_friendship['status']])
        write_csv('friendship.csv', friendship_data)
        return jsonify({"message": "Amizade adicionada com sucesso", "friendship": new_friendship}), 201

    elif request.method == 'DELETE':
        # Defina valores padrão para os parâmetros
        user1_id = request.args.get('user1_id', '')
        user2_id = request.args.get('user2_id', '')
        friendship_id = user1_id + '-' + user2_id

        friendship_data = read_csv('friendship.csv')
        friendship_data = [friendship for friendship in friendship_data if f"{friendship[0]}-{friendship[1]}" != friendship_id]
        write_csv('friendship.csv', friendship_data)
        return jsonify({"message": "Amizade removida com sucesso"})


# Endpoint para gerenciar postagens (Criar, Editar, Excluir)
@app.route('/postagens/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gerenciar_postagens():
    """
    Gerenciar postagens (Criar, Editar, Excluir)
    ---
    tags:
      - Postagens
    responses:
      200:
        description: Operação realizada com sucesso
    """
    if request.method == 'GET':
        posts_data = read_csv('posts.csv')
        return jsonify({"posts": posts_data})

    elif request.method == 'POST':
        # Criar uma nova postagem
        new_post = request.json
        posts_data = read_csv('posts.csv')
        posts_data.append([new_post['user_id'], new_post['titulo'], new_post['conteudo'], new_post['data_postagem']])
        write_csv('posts.csv', posts_data)
        return jsonify({"message": "Postagem criada com sucesso", "post": new_post}), 201

    elif request.method == 'PUT':
        # Editar uma postagem existente
        updated_post = request.json
        posts_data = read_csv('posts.csv')
        for post in posts_data:
            if post[0] == updated_post['user_id'] and post[1] == updated_post['titulo']:
                post[2] = updated_post['conteudo']
                post[3] = updated_post['data_postagem']
                break
        write_csv('posts.csv', posts_data)
        return jsonify({"message": "Postagem atualizada com sucesso", "post": updated_post})

    elif request.method == 'DELETE':
        # Defina valores padrão para os parâmetros
        user_id = request.args.get('user_id', '')
        titulo = request.args.get('titulo', '')
        post_id = user_id + '-' + titulo

        posts_data = read_csv('posts.csv')
        posts_data = [post for post in posts_data if f"{post[0]}-{post[1]}" != post_id]
        write_csv('posts.csv', posts_data)
        return jsonify({"message": "Postagem excluída com sucesso"})


# Execução da aplicação Flask
if __name__ == "__main__":
    app.run(debug=True)
