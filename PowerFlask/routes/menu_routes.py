from flask import Blueprint, render_template
from flask_login import login_required, current_user
from PowerFlask.utils.menu_utils import get_user_data

# Cria um Blueprint para as rotas do menu e do perfil
menu_bp = Blueprint('menu', __name__)

# Rota para a página inicial do menu
@menu_bp.route('/')
@login_required  # Garante que o usuário esteja autenticado para acessar essa rota
def index():
    # Renderiza a página index.html, passando o usuário atual como contexto
    return render_template('index.html', user=current_user)

# Rota para a página de perfil do usuário
@menu_bp.route('/profile')
@login_required  # Garante que o usuário esteja autenticado para acessar essa rota
def profile():
    # Obtém o token de acesso do usuário autenticado
    access_token = current_user.access_token

    # Obtém os dados do usuário da API Graph da Microsoft
    user_data = get_user_data(access_token)

    # Renderiza a página profile.html, passando os dados do usuário como contexto
    return render_template('profile.html', user=user_data)
