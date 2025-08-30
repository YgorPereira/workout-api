from typing import Annotated
from pydantic import UUID4

from pydantic import Field
from workout_api.contrib.schemas import BaseSchema


class CentroTreinamento(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Centro de Treinamento', example='CT Cariani', max_length=50)]
    endereco: Annotated[str, Field(description='Endereço do Centro de Treinamento', example='Bairro jardim das flores, rua das andorinhas, 42', max_length=100)]
    proprietario: Annotated[str, Field(description='Nome do Proprietário', example='Renato Cariani', max_length=50)]


class CentroTreinamentoIn(CentroTreinamento):
    pass


class CentroTreinamentoOut(CentroTreinamento):
    id: Annotated[UUID4, Field(description='Identificação do CT')]


class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Centro de Treinamento', example='CT Cariani', max_length=50)]