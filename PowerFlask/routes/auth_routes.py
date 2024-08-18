from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import login_user, logout_user, login_required
import logging
from PowerFlask.utils.auth_utils import get_auth_url, acquire_token_by_code
from PowerFlask.models.user_models import User, UserStorage

# Cria um Blueprint para as rotas de autenticação
auth_bp = Blueprint('auth', __name__)

# Rota para a página de login
@auth_bp.route("/login")
def login():
    # Gera a URL de autorização para autenticação
    auth_url = get_auth_url()
    # Renderiza a página de login, passando a URL de autorização como contexto
    return render_template('login.html', auth_url=auth_url)

# Configuração de logging para depuração
logging.basicConfig(level=logging.DEBUG)

# Rota para receber o token de acesso após a autenticação
@auth_bp.route("/getAToken")
def get_token():
    logging.debug("Received request for /getAToken")
    # Obtém o código de autorização da requisição
    code = request.args.get('code')
    if not code:
        logging.error("No code found in request")
        return "No code found", 400

    # Adquire o token de acesso usando o código de autorização
    result = acquire_token_by_code(code)

    if "access_token" in result:
        # Obtém as informações do usuário do token
        user_info = result.get("id_token_claims")
        # Cria um objeto User e armazena-o no UserStorage
        user = User(user_info["oid"], user_info["name"], user_info["preferred_username"], access_token=result["access_token"])
        UserStorage.add(user)
        # Faz login do usuário
        login_user(user)
        logging.debug(f"User {user.name} logged in successfully")
        # Redireciona para a página inicial do menu
        return redirect(url_for("menu.index"))
    else:
        error = result.get("error")
        error_description = result.get("error_description")
        logging.error(f"Login failed: {error} - {error_description}")
        # Retorna mensagem de falha no login
        return f"Login failed: {error} - {error_description}", 401

# Rota para fazer logout do usuário
@auth_bp.route("/logout")
@login_required # Garante que o usuário esteja autenticado para acessar essa rota
def logout():
    # Faz logout do usuário
    logout_user()
    # Redireciona o usuário de volta à página de login
    return redirect(url_for('auth.login'))
