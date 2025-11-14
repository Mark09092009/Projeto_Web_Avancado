from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='E-mail',  
        required=True,  
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}) 
    )
    first_name = forms.CharField(label='Nome', required=False) 
    last_name = forms.CharField(label='Sobrenome', required=False)  
    def save(self, commit=True):
        
        user = super().save(commit=False)
        
        base_username = self.cleaned_data["email"].split('@')[0]
        unique_username = base_username
        counter = 1
        
        while User.objects.filter(username=unique_username).exists():
            unique_username = f"{base_username}_{counter}"
            counter += 1
        user.username = unique_username 


        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
        return user

    class Meta(UserCreationForm.Meta):
        model = User  
        fields = ('email', 'first_name', 'last_name') + UserCreationForm.Meta.fields[1:]

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_("E-mail"),  
        max_length=254,  
        widget=forms.EmailInput(attrs={
            'autofocus': True,  
            'class': 'form-control', 
            'placeholder': 'Seu e-mail'
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