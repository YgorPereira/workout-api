from typing import Annotated

from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchema


class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description="Nome da categoria", examples=["Scale"], max_length=50)]

class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(description='identificador da categoria', examples=['123e4567-e89b-12d3-a456-426614174000'])]
