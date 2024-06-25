# main/urls.py

from django.urls import include, path
from .views import CustomLoginView, custom_logout, home, veiculos, adicionar_veiculo, gerenciar_veiculo, veiculos_agendados, manutencoes, agendar_manutencao, editar_manutencao, excluir_manutencao, relatorio_veiculos, relatorio_manutencoes, contato
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # Página inicial
    path('', home, name='home'),

    # Veículos
    path('veiculos/', login_required(veiculos), name='veiculos'),
    path('veiculo/adicionar/', login_required(adicionar_veiculo), name='adicionar_veiculo'),
    path('veiculo/<int:veiculo_id>/', login_required(gerenciar_veiculo), name='editar_veiculo'),
    path('veiculos/agendados/', login_required(veiculos_agendados), name='veiculos_agendados'),

    # Manutenções
    path('manutencoes/', login_required(manutencoes), name='manutencoes'),
    path('manutencoes/agendar/', login_required(agendar_manutencao), name='agendar_manutencao'),
    path('manutencao/editar/<int:manutencao_id>/', login_required(editar_manutencao), name='editar_manutencao'),
    path('manutencao/excluir/<int:manutencao_id>/', login_required(excluir_manutencao), name='excluir_manutencao'),

    # Relatórios
    path('relatorio/veiculos/', login_required(relatorio_veiculos), name='relatorio_veiculos'),
    path('relatorio/manutencoes/', login_required(relatorio_manutencoes), name='relatorio_manutencoes'),

    # Autenticação
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),

    # Contato
    path('contato/', login_required(contato), name='contato'),
]

