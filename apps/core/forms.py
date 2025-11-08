# Seu_App/forms.py

# Se você já tem um CustomUserCreationForm no mesmo arquivo, ele deve estar aqui também.
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import AuthenticationForm 
from django.utils.translation import gettext_lazy as _

# Cria uma classe de formulário que herda do UserCreationForm
class CustomUserCreationForm(UserCreationForm):
    # 1. Campos personalizados (mantidos)
    email = forms.EmailField(
        label='E-mail',
        required=True, # Torna o campo obrigatório
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    
    first_name = forms.CharField(label='Nome', required=False)
    last_name = forms.CharField(label='Sobrenome', required=False)

    # 2. O método 'save' modificado para gerar o username
    def save(self, commit=True):
        # Chama o save original, mas NÃO salva no banco ainda (commit=False)
        user = super().save(commit=False) 
        
        # ⚠️ PASSO CRÍTICO: Geração automática e única do username
        # O Django exige um username. Usamos o e-mail como base.
        base_username = self.cleaned_data["email"].split('@')[0]
        
        # Garante que o username gerado é único
        unique_username = base_username
        counter = 1
        while User.objects.filter(username=unique_username).exists():
            unique_username = f"{base_username}_{counter}"
            counter += 1
            
        user.username = unique_username
        
        # Atribui os campos extras do formulário
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        
        if commit:
            user.save()
        return user
    
    # 3. Meta atualizada para excluir 'username'
    class Meta(UserCreationForm.Meta):
        model = User
        
        # Define os campos EXATAMENTE como você quer: 
        # email, nome, sobrenome, e os campos de senha (herdados por fatiamento)
        # UserCreationForm.Meta.fields[1:] omite o primeiro item ('username')
        fields = ('email', 'first_name', 'last_name') + UserCreationForm.Meta.fields[1:]

class EmailAuthenticationForm(AuthenticationForm):
    """
    Formulário de Autenticação personalizado para usar "E-mail" como rótulo 
    principal de login em vez de "Nome de Usuário".
    """
    # 1. Sobrescreve o campo 'username' para garantir o rótulo e o widget corretos.
    username = forms.CharField(
        label=_("E-mail"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Seu e-mail'})
    )
    
    # 2. Sobrescreve o campo 'password' para garantir o rótulo e a classe CSS.
    password = forms.CharField(
        label=_("Senha"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Sua senha'})
    )

    # Nota: O seu backend de autenticação (settings.py) precisa estar configurado 
    # para permitir login via e-mail se você estiver usando e-mail. 
    # Por padrão, o Django usa o campo 'username'.