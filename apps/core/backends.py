from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

# Obtém o modelo de usuário ativo
UserModel = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Este backend permite que o usuário faça login usando o nome de usuário (username)
    OU o e-mail, em conjunto com a senha.
    
    Ele estende o ModelBackend padrão do Django.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # O campo é chamado 'username' na função, mas pode conter um e-mail.
        try:
            # Tenta encontrar um usuário cujo 'username' (o que o usuário digitou)
            # corresponda ao campo 'username' OU ao campo 'email' na base de dados.
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            # Se o usuário não for encontrado com username ou email, retorna None
            return None
        
        # Verifica a senha do usuário encontrado
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None