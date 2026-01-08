from django import forms
from .models import Cliente, Funcionario
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_("E-mail ou usuário"),
        max_length=254,
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'form-control',
            'placeholder': 'E-mail ou nome de usuário'
        })
    )
    
    
    password = forms.CharField(
        label=_("Senha"),
        strip=False, 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',  
            'placeholder': 'Sua senha' 
        })
    )

class ContatoForm(forms.Form):
    nome = forms.CharField(
        max_length=100, 
        label='Seu Nome',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Seu E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    assunto = forms.CharField(
        max_length=100, 
        required=False, 
        label='Assunto',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    mensagem = forms.CharField(
        label='Mensagem',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}) 
    )

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        
        # 2. Quais campos do modelo devem aparecer no formulário?
        # Excluímos 'user' porque ele é uma chave estrangeira
        # e é geralmente gerenciado no código da view (não diretamente pelo usuário).
        fields = [
            'full_name', 
            'cpf', 
            'email',
            'endereco',
        ]
        labels = {
            'full_name': 'Nome Completo',
            'cpf': 'CPF',
            'email': 'E-mail',
            'endereco': 'Endereço',
        }

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
    
        # 2. Quais campos do modelo devem aparecer no formulário?
        fields = [
            'full_name', 
            'job_title', 
            'salary', 
            'is_manager'
        ]
        labels = {
            'full_name': 'Nome Completo',
            'job_title': 'Cargo',
            'salary': 'Salário Mensal',
            'is_manager': 'Função de Gerência',
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nome de usuário'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirme a senha'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email', '')
        if commit:
            user.save()
        return user
        widgets = {

            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply bootstrap classes to form fields
        for name, field in self.fields.items():
            if name == 'is_manager':
                field.widget.attrs.update({'class': 'form-check-input'})
            elif name == 'hire_date':
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-control'})