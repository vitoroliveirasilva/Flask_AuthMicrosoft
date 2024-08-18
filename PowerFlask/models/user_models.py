from flask_login import UserMixin

class User(UserMixin):
    """
    Classe que representa um usuário autenticado.

    Herda de UserMixin, que fornece implementações padrão para os métodos necessários
    para gerenciar a autenticação de usuários no Flask-Login.

    Atributos:
        id (str): Identificador único do usuário (normalmente o Object ID do Azure AD).
        name (str): Nome do usuário.
        email (str): Endereço de email do usuário.
        access_token (str): Token de acesso utilizado para fazer chamadas autenticadas à API Graph da Microsoft.
    """
    def __init__(self, user_id, name, email, access_token=None):
        """
        Inicializa uma nova instância da classe User.

        Args:
            user_id (str): O ID do usuário.
            name (str): O nome do usuário.
            email (str): O email do usuário.
            access_token (str, opcional): Token de acesso do usuário para chamadas à API Graph.
        """
        self.id = user_id
        self.name = name
        self.email = email
        self.access_token = access_token

    @staticmethod
    def get(user_id):
        """
        Recupera um usuário do armazenamento usando seu ID.

        Args:
            user_id (str): O ID do usuário.

        Returns:
            User: Uma instância da classe User se o usuário for encontrado, caso contrário None.
        """
        return UserStorage.get(user_id)


class UserStorage:
    """
    Classe que simula o armazenamento de usuários em memória.

    Atributos:
        users (dict): Um dicionário que mapeia IDs de usuários para instâncias da classe User.
    """
    users = {}

    @staticmethod
    def add(user):
        """
        Adiciona um usuário ao armazenamento.

        Args:
            user (User): A instância do usuário a ser adicionada ao armazenamento.
        """
        UserStorage.users[user.id] = user

    @staticmethod
    def get(user_id):
        """
        Recupera um usuário do armazenamento usando seu ID.

        Args:
            user_id (str): O ID do usuário.

        Returns:
            User: Uma instância da classe User se o usuário for encontrado, caso contrário None.
        """
        return UserStorage.users.get(user_id)
