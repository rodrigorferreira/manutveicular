from ninja import NinjaAPI
from .models import Veiculo, Manutencao
from django.shortcuts import get_object_or_404
from .schemas import VeiculoSchema, ManutencaoSchema

api = NinjaAPI()

@api.get("/veiculos", response=VeiculoSchema)
def list_veiculos(request):
    return Veiculo.objects.all()

@api.get("/veiculos/{veiculo_id}", response=VeiculoSchema)
def get_veiculo(request, veiculo_id: int):
    return get_object_or_404(Veiculo, id=veiculo_id)

@api.post("/veiculos", response=VeiculoSchema)
def create_veiculo(request, data: VeiculoSchema):
    veiculo = Veiculo(**data.dict())
    veiculo.save()
    return veiculo

@api.get("/manutencoes", response=ManutencaoSchema)
def list_manutencoes(request):
    return Manutencao.objects.all()

@api.post("/manutencoes", response=ManutencaoSchema)
def create_manutencao(request, data: ManutencaoSchema):
    manutencao = Manutencao(**data.dict())
    manutencao.save()
    return manutencao
