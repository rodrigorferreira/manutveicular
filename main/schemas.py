from ninja import Schema

class VeiculoSchema(Schema):
    id: int
    usuario_id: int
    placa: str
    modelo: str
    marca: str
    ano: int
    cor: str
    km_atual: int

class ManutencaoSchema(Schema):
    id: int
    veiculo_id: int
    descricao: str
    data_manutencao: str
    custo: float
