from dataclasses import field
from pydantic import Field, PositiveFloat
from typing import Annotated, Optional

from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta
from workout_api.contrib.schemas import BaseSchema, OutMixin


class Atleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", example='João Silva', max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", example='12345678901', max_length=11)]
    idade: Annotated[int, Field(description="Idade do atleta", example=30)]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta em kg", example=70.5)]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta em metros", example=1.75)]
    sexo: Annotated[str, Field(description="Sexo do atleta", example='M', max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description="Categoria do atelta")]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description="Categoria do atelta")]


class AtletaIn(Atleta):
    pass


class AtletaOut(Atleta, OutMixin):
    pass


class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], str, Field(None, description="Nome do atleta", example='João Silva', max_length=50)]
    idade: Annotated[Optional[int], int, Field(None, description="Idade do atleta", example=30)]