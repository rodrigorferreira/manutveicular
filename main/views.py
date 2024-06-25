# main/views.py
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from .models import Veiculo, Manutencao
from .forms import VeiculoForm, ManutencaoForm
from django.conf import settings
from .forms import ManutencaoForm

# Views relacionadas à autenticação
# Custom login view
class CustomLoginView(LoginView):
    template_name = 'main/login.html'

# View para fazer logout

def custom_logout(request):
    logout(request)
    return redirect('login')

# View para a página inicial (acessível sem autenticação)

def home(request):
    return render(request, 'main/home.html')

# View para a página de contato

def contato(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        mensagem = request.POST.get('mensagem')

        # Envia um e-mail com a mensagem de contato
        send_mail(
            'Nova mensagem de contato',
            f'Você recebeu uma nova mensagem de {nome} ({email}): \n\n{mensagem}',
            settings.EMAIL_HOST_USER,
            ['rrodrigues.dev@outlook.com'],  # Substitua pelo seu e-mail onde deseja receber as mensagens
            fail_silently=False,
        )
        return redirect('home')  # Redireciona para a página inicial após o envio bem-sucedido
    else:
        # Se não for uma requisição POST, apenas renderiza o formulário de contato
        return render(request, 'main/contato.html')

# Views relacionadas aos veículos
# View para listar, adicionar e editar veículos
@login_required
def veiculos(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            novo_veiculo = form.save(commit=False)
            novo_veiculo.usuario = request.user
            novo_veiculo.save()
            return redirect('veiculos')
    else:
        form = VeiculoForm()
    veiculos_list = Veiculo.objects.filter(usuario=request.user)
    return render(request, 'main/veiculos.html', {'veiculos': veiculos_list, 'form': form})

# View para adicionar um novo veículo
@login_required
def adicionar_veiculo(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            novo_veiculo = form.save(commit=False)
            novo_veiculo.usuario = request.user
            novo_veiculo.save()
            return redirect('veiculos')
    else:
        form = VeiculoForm()
    return render(request, 'main/veiculo_form.html', {'form': form})

# View para editar um veículo existente
@login_required
def editar_veiculo(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, pk=veiculo_id, usuario=request.user)
    if request.method == 'POST':
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            return redirect('veiculos')
    else:
        form = VeiculoForm(instance=veiculo)
    return render(request, 'main/veiculos.html', {'form': form, 'veiculo_id': veiculo_id})

# View para listar os veículos que têm alguma manutenção agendada
@login_required
def veiculos_agendados(request):
    # Filtra os veículos que têm alguma manutenção agendada
    veiculos = Veiculo.objects.filter(usuario=request.user, manutencao__isnull=False).distinct()
    # Passa os veículos para o template
    return render(request, 'main/veiculos_agendados.html', {'veiculos': veiculos})

# View para gerenciar veículos
@login_required
def gerenciar_veiculo(request, veiculo_id=None):
    # Se o veiculo_id for fornecido, obtém o veículo correspondente
    if veiculo_id:
        veiculo = get_object_or_404(Veiculo, pk=veiculo_id, usuario=request.user)
        form = VeiculoForm(request.POST or None, instance=veiculo)
    # Se não, cria um novo formulário vazio
    else:
        form = VeiculoForm(request.POST or None)
    # Se a requisição for POST e o formulário for válido, salva o veículo
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('veiculos')
    # Se não, renderiza o template com o formulário e a lista de veículos
    veiculos_list = Veiculo.objects.filter(usuario=request.user)
    return render(request, 'main/gerenciar_veiculo.html', {'form': form, 'veiculos': veiculos_list, 'veiculo_id': veiculo_id})

# Views relacionadas às manutenções
# View para listar as manutenções cadastradas
@login_required
def manutencoes(request):
    if request.method == 'POST':
        form = ManutencaoForm(request.POST)
        if form.is_valid():
            manutencao = form.save(commit=False)
            manutencao.usuario = request.user  # Atribui o usuário logado ao campo usuario
            manutencao.save()
            return redirect('manutencoes')
    else:
        form = ManutencaoForm()
    manutencoes = Manutencao.objects.all()
    veiculos = Veiculo.objects.all()
    context = {
        'form': form,           # Certifique-se de que o formulário está sendo passado no contexto
        'manutencoes': manutencoes,
        'veiculos': veiculos,
    }
    return render(request, 'main/manutencoes.html', context)

# View para agendar uma nova manutenção
@login_required
def agendar_manutencao(request):
    if request.method == 'POST':
        form = ManutencaoForm(request.POST)
        if form.is_valid():
            manutencao = form.save(commit=False)
            manutencao.usuario = request.user
            manutencao.save()
            return redirect('manutencoes')
    else:
        form = ManutencaoForm()
    # Filtra os veículos do usuário logado
    veiculos = Veiculo.objects.filter(usuario=request.user)
    # Filtra as manutenções do usuário logado
    manutencoes = Manutencao.objects.filter(veiculo__usuario=request.user)
    # Passa os veículos e as manutenções para o template
    return render(request, 'main/manutencoes.html', {'form': form, 'veiculos': veiculos, 'manutencoes': manutencoes})

@login_required
def editar_manutencao(request, manutencao_id):
    manutencao = get_object_or_404(Manutencao, pk=manutencao_id, usuario=request.user)
    if request.method == 'POST':
        form = ManutencaoForm(request.POST, instance=manutencao)
        if form.is_valid():
            form.save()
            return redirect('manutencoes')
    else:
        form = ManutencaoForm(instance=manutencao)
    return render(request, 'main/editar_manutencao.html', {'form': form})


@login_required
def excluir_manutencao(request, manutencao_id):
    manutencao = get_object_or_404(Manutencao, id=manutencao_id)
    manutencao.delete()
    return redirect('manutencoes')

@login_required
def listar_manutencoes(request):
    manutencoes = Manutencao.objects.filter(usuario=request.user)
    return render(request, 'main/manutencoes.html', {'manutencoes': manutencoes})

@login_required
def relatorio_veiculos(request):
    veiculos = Veiculo.objects.all()
    return render(request, 'main/relatorio_veiculos.html', {'veiculos': veiculos})

@login_required
def relatorio_manutencoes(request):
    manutencoes = Manutencao.objects.all()
    return render(request, 'main/relatorio_manutencoes.html', {'manutencoes': manutencoes})