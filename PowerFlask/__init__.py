from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_session import Session
from app_config import config

# Instancia o gerenciador de login do Flask-Login
login_manager = LoginManager()

# Define o manipulador de redirecionamento quando um usuário não autenticado tenta acessar uma rota protegida
@login_manager.unauthorized_handler
def unauthorized():
    # Redireciona o usuário não autenticado para a página de login
    return redirect(url_for('auth.login'))

# Define o carregador de usuário necessário para o Flask-Login
@login_manager.user_loader
def load_user(user_id):
    # Importa o modelo de usuário para buscar o usuário a partir do ID
    from PowerFlask.models.user_models import User
    return User.get(user_id)

# Função de fábrica para criar e configurar a aplicação Flask
def create_app():
    # Cria a instância do aplicativo Flask
    app = Flask(__name__)
    # Carrega as configurações a partir do objeto config
    app.config.from_object(config)

    # Inicializa o gerenciador de login com o aplicativo
    login_manager.init_app(app)
    # Configura o gerenciamento de sessões no Flask
    Session(app)

    # Importa e registra os Blueprints de rotas
    from PowerFlask.routes.auth_routes import auth_bp
    from PowerFlask.routes.menu_routes import menu_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(menu_bp)

    # Retorna a instância configurada do aplicativo Flask
    return app
