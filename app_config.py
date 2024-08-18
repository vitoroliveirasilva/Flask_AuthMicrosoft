from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente a partir de um arquivo .env, facilitando a configuração de credenciais e outros parâmetros sensíveis
load_dotenv()

class Config:
    # Configurações gerais do aplicativo, como chave secreta, ID do cliente, segredo do cliente e outros
    SECRET_KEY = os.getenv('SECRET_KEY')  # Chave secreta usada para segurança do Flask (por exemplo, proteção contra CSRF)
    CLIENT_ID = os.getenv('CLIENT_ID')  # ID do cliente registrado no Azure AD
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')  # Segredo do cliente registrado no Azure AD
    AUTHORITY = f"https://login.microsoftonline.com/{os.getenv('TENANT_ID')}"  # URL de autoridade do Azure AD, usando o ID do locatário
    REDIRECT_PATH = "/getAToken"  # Caminho de redirecionamento após a autenticação, definido no azuro como http://localhost:5000/getAToken
    SCOPE = ["User.Read"]  # Escopo de permissões solicitadas durante a autenticação
    SESSION_TYPE = "filesystem"  # Tipo de sessão usada pelo Flask; "filesystem" indica que as sessões serão armazenadas em arquivos

# Instancia o objeto de configuração para ser utilizado pelo aplicativo
config = Config()
