from flask import url_for
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
        code, scopes=config.SCOPE, redirect_uri=url_for('auth.get_token', _external=True)
    )
