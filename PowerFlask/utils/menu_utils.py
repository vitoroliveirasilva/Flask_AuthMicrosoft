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
