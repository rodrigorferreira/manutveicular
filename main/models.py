from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django_cpf_cnpj.fields import CPFField, CNPJField

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    cpf = CPFField(masked=True, unique=True, null=True, blank=True)  # CPF do usuário
    cnpj = CNPJField(masked=True, unique=True, null=True, blank=True)  # CNPJ do usuário
    is_company = models.BooleanField(default=False)  # Diferenciar se é empresa (CNPJ) ou pessoa física (CPF)

    def __str__(self):
        return self.email

class Veiculo(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    placa = models.CharField(max_length=7, unique=True)
    modelo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    ano = models.IntegerField()
    cor = models.CharField(max_length=30)
    km_atual = models.IntegerField()

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa})"

class Manutencao(models.Model):
    STATUS_CHOICES = [
        ('agendado', 'Agendado'),
        ('em_andamento', 'Em andamento'),
        ('concluido', 'Concluído'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    descricao = models.TextField()
    data_manutencao = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='agendado')

    def __str__(self):
        return f"{self.veiculo} - {self.descricao} - {self.get_status_display()}"