from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4

from workout_api import categorias
from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy import select


router = APIRouter()


@router.post('/', summary="Criar uma nova categoria", status_code=status.HTTP_201_CREATED, response_model=CategoriaOut,)
async def post(db_session: DatabaseDependency, categoria_in: CategoriaIn = Body(...)) -> CategoriaOut:
    try:
        categoria_model = CategoriaModel(
            nome=categoria_in.nome,
        )

        db_session.add(categoria_model)
        await db_session.commit()
        await db_session.refresh(categoria_model)

        atleta_out = CategoriaOut(
            id=uuid4(),
            nome=categoria_model.nome
        )

        return atleta_out
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao categoria: {str(e)}",
        )


@router.get('/', summary="Consultar todas as categorias", status_code=status.HTTP_200_OK, response_model=list[CategoriaOut],)
async def get(db_session: DatabaseDependency) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()

    return categorias


@router.get('/{id}', summary="Consultar categoria por id", status_code=status.HTTP_200_OK, response_model=CategoriaOut,)
async def get_by_id(id: UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()

    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Categoria não encontrada no id: {id}')

    return categoria
