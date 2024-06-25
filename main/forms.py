# main/forms.py

from django import forms
from .models import Veiculo
from .models import Manutencao
from django.utils import timezone

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa', 'modelo', 'marca', 'ano', 'cor', 'km_atual']

class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = ['veiculo', 'descricao', 'data_manutencao', 'status']
        widgets = {
            'veiculo': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'data_manutencao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ManutencaoForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            self.fields['data_manutencao'].widget = forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }, format='%Y-%m-%d')
            instance = kwargs['instance']