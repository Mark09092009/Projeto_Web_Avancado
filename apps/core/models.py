from django.contrib.auth.models import User
from django.db import models

class Cliente(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        primary_key=True
    )
    # Informações específicas do Cliente
    full_name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=18, unique=True, verbose_name="CPF")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    endereco = models.CharField(max_length=255, verbose_name="Endereço", blank=True, null=True)

    def __str__(self):
        return self.full_name
    
class Funcionario(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        primary_key=True
    )
    employee_id_number = models.CharField(max_length=20, unique=True, verbose_name="Matrícula")
    full_name = models.CharField(max_length=255)
    hire_date = models.DateField(verbose_name="Data de Contratação")
    job_title = models.CharField(max_length=100, verbose_name="Cargo")
    
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_manager = models.BooleanField(default=False, verbose_name="É Gerente")
    def __str__(self):
        return f"{self.full_name} ({self.job_title})"