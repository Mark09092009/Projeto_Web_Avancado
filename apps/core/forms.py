# Importa os módulos necessários do Django
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Criação de um formulário personalizado para registro de usuários
class CustomUserCreationForm(UserCreationForm):
    # Adiciona campos personalizados ao formulário de registro
    email = forms.EmailField(
        label='E-mail',  # Rótulo do campo
        required=True,  # Torna o campo obrigatório
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})  # Define o widget HTML
    )
    first_name = forms.CharField(label='Nome', required=False)  # Campo opcional para o primeiro nome
    last_name = forms.CharField(label='Sobrenome', required=False)  # Campo opcional para o sobrenome

    # Sobrescreve o método 'save' para personalizar o comportamento ao salvar o usuário
    def save(self, commit=True):
        # Chama o método 'save' da classe pai, mas não salva no banco ainda (commit=False)
        user = super().save(commit=False)
        
        # Gera um username único baseado no e-mail do usuário
        base_username = self.cleaned_data["email"].split('@')[0]  # Usa a parte antes do '@' como base
        unique_username = base_username
        counter = 1
        # Verifica se o username já existe e adiciona um sufixo numérico se necessário
        while User.objects.filter(username=unique_username).exists():
            unique_username = f"{base_username}_{counter}"
            counter += 1
        user.username = unique_username  # Define o username gerado

        # Atribui os valores dos campos adicionais ao objeto do usuário
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        # Salva o usuário no banco de dados se 'commit' for True
        if commit:
            user.save()
        return user

    # Define a classe Meta para configurar o formulário
    class Meta(UserCreationForm.Meta):
        model = User  # Modelo associado ao formulário
        # Define os campos do formulário, excluindo 'username' e mantendo os campos de senha
        fields = ('email', 'first_name', 'last_name') + UserCreationForm.Meta.fields[1:]

# Criação de um formulário de autenticação personalizado
class EmailAuthenticationForm(AuthenticationForm):
    """
    Formulário de autenticação que utiliza o e-mail como principal campo de login,
    em vez do nome de usuário padrão.
    """
    # Sobrescreve o campo 'username' para usar o e-mail como rótulo e widget
    username = forms.CharField(
        label=_("E-mail"),  # Rótulo do campo
        max_length=254,  # Tamanho máximo do campo
        widget=forms.EmailInput(attrs={
            'autofocus': True,  # Foco automático no campo
            'class': 'form-control',  # Classe CSS para estilização
            'placeholder': 'Seu e-mail'  # Placeholder no campo
        })
    )
    
    # Sobrescreve o campo 'password' para personalizar o rótulo e o widget
    password = forms.CharField(
        label=_("Senha"),  # Rótulo do campo
        strip=False,  # Permite espaços em branco na senha
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',  # Classe CSS para estilização
            'placeholder': 'Sua senha'  # Placeholder no campo
        })
    )

    # Nota: Para que o login funcione com e-mail, o backend de autenticação no settings.py
    # deve ser configurado para aceitar e-mails como credenciais de login.
