from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

# Obtém o modelo de usuário ativo configurado no projeto Django
UserModel = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    """
    EmailOrUsernameModelBackend é uma classe personalizada que estende o backend padrão de autenticação do Django, 
    permitindo que os usuários façam login utilizando tanto o nome de usuário (username) quanto o e-mail, 
    em conjunto com a senha.

    Métodos:
    ---------
    1. authenticate(self, request, username=None, password=None, **kwargs):
        - Este método tenta autenticar um usuário com base no nome de usuário ou e-mail fornecido, 
          juntamente com a senha.
        - Ele utiliza uma consulta para verificar se existe um usuário cujo 'username' ou 'email' 
          corresponde ao valor fornecido.
        - Caso um usuário seja encontrado, verifica se a senha fornecida corresponde à senha armazenada.
        - Retorna o objeto do usuário autenticado se a autenticação for bem-sucedida, ou None caso contrário.

    2. get_user(self, user_id):
        - Este método é responsável por obter um usuário com base no ID fornecido.
        - Ele retorna o objeto do usuário correspondente ao ID, ou None se o usuário não for encontrado.

    Uso:
    -----
    - Este backend é útil em cenários onde se deseja oferecer flexibilidade para os usuários fazerem login 
      tanto com o nome de usuário quanto com o e-mail.
    - Deve ser configurado no projeto Django como um backend de autenticação personalizado.

    Exemplo de Configuração:
    -------------------------
    No arquivo settings.py do projeto Django, adicione o caminho completo para esta classe na lista `AUTHENTICATION_BACKENDS`:
        AUTHENTICATION_BACKENDS = [
            'apps.core.backends.EmailOrUsernameModelBackend',
            'django.contrib.auth.backends.ModelBackend',  # Backend padrão do Django
        ]

    Notas:
    ------
    - Certifique-se de que o modelo de usuário utilizado no projeto possui os campos 'username' e 'email'.
    - Este backend não suporta autenticação de usuários inativos ou bloqueados, pois utiliza o comportamento padrão do Django.
    """
    """
    Este backend permite que o usuário faça login usando o nome de usuário (username)
    OU o e-mail, em conjunto com a senha.
    
    Ele estende o ModelBackend padrão do Django.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Método de autenticação que tenta autenticar um usuário com base no nome de usuário
        ou e-mail fornecido, juntamente com a senha.
        
        Args:
            request: O objeto de requisição HTTP (opcional).
            username: O nome de usuário ou e-mail fornecido pelo usuário.
            password: A senha fornecida pelo usuário.
            **kwargs: Argumentos adicionais.

        Returns:
            O objeto do usuário autenticado, ou None se a autenticação falhar.
        """
        try:
            # Tenta encontrar um usuário cujo 'username' ou 'email' corresponda ao valor fornecido.
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            # Retorna None se nenhum usuário for encontrado com o username ou email fornecido.
            return None
        
        # Verifica se a senha fornecida corresponde à senha do usuário encontrado.
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        """
        Método para obter um usuário com base no ID do usuário.

        Args:
            user_id: O ID do usuário.

        Returns:
            O objeto do usuário correspondente ao ID fornecido, ou None se não for encontrado.
        """
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            # Retorna None se o usuário com o ID fornecido não existir.
            return None