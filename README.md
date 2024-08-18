# Projeto Flask com Autenticação Microsoft Entra ID

Este projeto é uma aplicação Flask que utiliza a autenticação via Microsoft Entra ID (anteriormente conhecido como Microsoft Identity Platform). Ele permite que usuários façam login usando suas credenciais Microsoft e acessem informações do perfil obtidas da Microsoft Graph API.

## Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Configuração do Ambiente](#configuração-do-ambiente)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Arquivos de Configuração](#arquivos-de-configuração)
5. [Roteamento e Funcionalidade](#roteamento-e-funcionalidade)
6. [Executando a Aplicação](#executando-a-aplicação)
7. [Organização de Estilos e Comentários](#organização-de-estilos-e-comentários)
8. [Licença](#licença)

## Pré-requisitos

Antes de começar, você precisará ter o Python e o pip instalados. Além disso, é necessário ter uma conta Microsoft e registrar uma aplicação no [Microsoft Azure](https://portal.azure.com/) para obter os IDs e segredos necessários para a autenticação.

## Configuração do Ambiente

1. **Clone o Repositório**

   ```bash
   git clone https://github.com/usuario/repo.git
   cd repo
   ```

2. **Crie um Ambiente Virtual**

   ```bash
   python -m venv venv
   ```

3. **Ative o Ambiente Virtual**

   - No Windows:

     ```bash
     venv\Scripts\activate
     ```

   - No macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Instale as Dependências**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure as Variáveis de Ambiente**

   Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:

   ```env
   CLIENT_ID=seu-client-id
   CLIENT_SECRET=seu-client-secret
   TENANT_ID=seu-tenant-id
   SECRET_KEY=sua-secret-key
   ```

   Substitua os valores pelos dados obtidos do Microsoft Azure.

## Estrutura do Projeto

A estrutura do projeto é a seguinte:

```
/py.PowerFlask_auth
│
├── app.py                    # Arquivo principal do aplicativo Flask
├── app_config.py             # Configurações de ambiente e variáveis sensíveis
├── .env                      # Variáveis de ambiente (não incluído no repositório)
├── /PowerFlask               # Diretório principal do aplicativo
│   ├── __init__.py           # Inicialização do aplicativo Flask
│   ├── /models               # Modelos de dados do aplicativo
│   │   ├── __init__.py
│   │   └── user_models.py    # Modelos para gerenciamento de usuários
│   ├── /routes               # Rotas do aplicativo
│   │   ├── __init__.py
│   │   ├── auth_routes.py    # Rotas de autenticação
│   │   └── menu_routes.py    # Rotas para o menu e perfil do usuário
│   ├── /utils                # Funções auxiliares para as rotas
│   │   ├── __init__.py
│   │   ├── auth_utils.py     # Funções auxiliares para autenticação
│   │   └── menu_utils.py     # Funções auxiliares para o menu
│   ├── /static               # Arquivos estáticos
│   │   ├── /assets           # Arquivos estáticos adicionais
│   │   │   ├── icons/        # Ícones utilizados na aplicação
│   │   │   └── images/       # Imagens utilizadas na aplicação
│   │   ├── /css/             # Arquivos de estilo (CSS)
│   │   └── /js/              # Arquivos JavaScript
│   └── /templates            # Templates HTML do Flask
│       ├── index.html        # Página principal do menu
│       └── login.html        # Página de login
│       └── profile.html      # Página de perfil do usuário
├── requirements.txt          # Dependências do projeto
└── README.md                 # Documentação do projeto
```

## Arquivos de Configuração

### `app.py`

Cria a instância do aplicativo Flask e configura o logging.

```python
from PowerFlask import create_app

# Cria a instância do aplicativo Flask
app = create_app()

# Configura o logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Executa o aplicativo
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
```

### `app_config.py`

Configura as variáveis de ambiente para o aplicativo Flask.

```python
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    AUTHORITY = f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}"
    REDIRECT_PATH = "/getAToken"
    SCOPE = ["User.Read"]
    SESSION_TYPE = "filesystem"

config = Config()
```

### `.env`

Arquivo contendo as variáveis de ambiente necessárias para a aplicação.

```env
CLIENT_ID=seu-client-id
CLIENT_SECRET=seu-client-secret
TENANT_ID=seu-tenant-id
SECRET_KEY=sua-secret-key
```

### `PowerFlask/__init__.py`

Configura e cria a aplicação Flask, inicializa o login e o gerenciamento de sessões.

```python
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_session import Session
from app_config import config

login_manager = LoginManager()

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))

@login_manager.user_loader
def load_user(user_id):
    from PowerFlask.models.user_models import User
    return User.get(user_id)

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    login_manager.init_app(app)
    Session(app)

    from PowerFlask.routes.auth_routes import auth_bp
    from PowerFlask.routes.menu_routes import menu_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(menu_bp)

    return app
```

### `PowerFlask/models/user_models.py`

Define o modelo `User` e a classe `UserStorage` para armazenar informações do usuário.

```python
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, name, email, access_token=None):
        self.id = user_id
        self.name = name
        self.email = email
        self.access_token = access_token

    @staticmethod
    def get(user_id):
        return UserStorage.get(user_id)

class UserStorage:
    users = {}

    @staticmethod
    def add(user):
        UserStorage.users[user.id] = user

    @staticmethod
    def get(user_id):
        return UserStorage.users.get(user_id)
```

### `PowerFlask/routes/auth_routes.py`

Define as rotas para autenticação, login e logout.

```python
from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import login_user, logout_user, login_required
import logging
from PowerFlask.utils.auth_utils import get_auth_url, acquire_token_by_code
from PowerFlask.models.user_models import User, UserStorage

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login")
def login():
    auth_url = get_auth_url()
    return render_template('login.html', auth_url=auth_url)

logging.basicConfig(level=logging.DEBUG)

@auth_bp.route("/getAToken")
def get_token():
    logging.debug("Received request for /getAToken")
    code = request.args.get('code')
    if not code:
        logging.error("No code found in request")
        return "No code found", 400

    result = acquire_token_by_code(code)

    if "access_token" in result:
        user_info = result.get("id_token_claims")
        user = User(user_info["oid"], user_info["name"], user_info["preferred_username"], access_token=result["access_token"])
        UserStorage.add(user)
        login_user(user)
        logging.debug(f"User {user.name} logged in successfully")
        return redirect(url_for("menu.index"))
    else:
        error = result.get("error")
        error_description = result.get("error_description")
        logging.error(f"Login failed: {error} - {error_description}")
        return f"Login failed: {error} - {error_description}", 401

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
```

### `PowerFlask/routes/menu_routes.py`

Define as rotas para o menu e o perfil do usuário.

```python
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from PowerFlask.utils.menu_utils import get_user_data

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/')
@login_required
def index():
    return render_template('index.html', user=current_user)

@menu_bp.route('/profile')
@login_required
def profile():
    access_token = current_user.access_token
    user_data = get_user_data(access_token)
    return render_template('profile.html', user=user_data)
```

### `PowerFlask/utils/auth_utils.py`

Contém funções auxiliares para a autenticação com a Microsoft Identity Platform.

```python
from msal import ConfidentialClientApplication
from app_config import config

def get_auth_url():
    """
    Gera a URL de autorização para autenticação com a Microsoft Identity Platform.

    Returns:
        str: URL de autorização.
    """
    client = ConfidentialClientApplication(
        config.CLIENT_ID, authority=config.AUTHORITY, client_credential=config.CLIENT_SECRET
    )
    return client.get_authorization_request_url(config.SCOPE, redirect_uri=url_for('auth.get_token', _external=True))

def acquire_token_by_code(code):
    """
    Adquire um token de acesso usando o código de autorização fornecido.

    Args:
        code (str): Código de autorização recebido.

    Returns:
        dict: Resultado da requisição para obter o token de acesso.
    """
    client = ConfidentialClientApplication(
        config.CLIENT_ID, authority=config.AUTHORITY, client_credential=config.CLIENT_SECRET
    )
    return client.acquire_token_by_authorization_code(
        code, scopes=config

.SCOPE, redirect_uri=url_for('auth.get_token', _external=True)
    )
```

### `PowerFlask/utils/menu_utils.py`

Contém funções auxiliares para manipulação de dados do menu e perfil.

```python
import requests

def get_user_data(access_token):
    """
    Obtém os dados do usuário da API Graph da Microsoft usando o token de acesso.

    Args:
        access_token (str): Token de acesso do usuário.

    Returns:
        dict: Dados do usuário retornados pela API.
    """
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    graph_url = 'https://graph.microsoft.com/v1.0/me'
    response = requests.get(graph_url, headers=headers)
    return response.json()
```

## Executando a Aplicação

Para executar a aplicação, use o seguinte comando:

```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`.

## Organização de Estilos e Comentários

O projeto inclui arquivos de estilo CSS localizados em [/PowerFlask/static/css/style.css](/PowerFlask/static/css/style.css). Além disso, foram adicionados comentários nos arquivos HTML e CSS para explicar as escolhas de design e estilo. No entanto, esses comentários não são o foco principal da documentação e, portanto, não estão incluídos neste README.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.