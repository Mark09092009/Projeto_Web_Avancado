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
    CARGOS = [
        ('GERENTE', 'Gerente'),
        ('FRENTISTA', 'Frentista'),
        ('CAIXA', 'Caixa'),
        ('MECANICO', 'Mecânico'),
        ('AUXILIAR', 'Auxiliar de Serviços Gerais'),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        primary_key=True
    )
    employee_id_number = models.CharField(max_length=20, unique=True, verbose_name="Matrícula", blank=True)
    full_name = models.CharField(max_length=255)
    hire_date = models.DateField(auto_now_add=True, verbose_name="Data de Contratação")
    job_title = models.CharField(
        max_length=20,
        choices=CARGOS,
        verbose_name="Cargo"
    )
    
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_manager = models.BooleanField(default=False, verbose_name="É Gerente")
    
    def save(self, *args, **kwargs):
        if not self.employee_id_number:
            # Generate matricula as EMP + pk, but since pk not set yet, use a counter or something
            # For simplicity, use a random or timestamp, but better to use pk after save
            super().save(*args, **kwargs)
            self.employee_id_number = f"EMP{self.pk:04d}"
            # Note: this will cause a second save, but it's fine
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.full_name} ({self.get_job_title_display()})"