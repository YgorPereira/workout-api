from uuid import uuid4
from pydantic import UUID4
from fastapi import APIRouter, Body, status, HTTPException

from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.contrib.dependencies import DatabaseDependency

from sqlalchemy import select

router = APIRouter()

@router.post('/', summary='Criar um novo centro de treinamento', status_code=status.HTTP_201_CREATED, response_model=CentroTreinamentoOut)
async def post(db_session: DatabaseDependency, centro_treinamento_in: CentroTreinamentoIn = Body(...)):
    try:
        centro_treinamento_model = CentroTreinamentoModel(
            nome=centro_treinamento_in.nome,
            endereco=centro_treinamento_in.endereco,
            proprietario=centro_treinamento_in.proprietario
        )

        db_session.add(centro_treinamento_model)
        await db_session.commit()
        await db_session.refresh(centro_treinamento_model)

        centro_treinamento_out = CentroTreinamentoOut(
            id=uuid4(),
            nome=centro_treinamento_model.nome,
            endereco=centro_treinamento_model.endereco,
            proprietario=centro_treinamento_model.proprietario
        )

        return centro_treinamento_out

    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar centro de treinamento: {str(e)}"
        )


@router.get('/', summary="Consultar todos os centro de treinamentos", status_code=status.HTTP_200_OK, response_model=list[CentroTreinamentoOut],)
async def get(db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
    centros_treinamento: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()

    return centros_treinamento


@router.get('/{id}', summary="Consultar centro de treinamento por id", status_code=status.HTTP_200_OK, response_model=CentroTreinamentoOut,)
async def get_by_id(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro_treinamento: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()

    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Categoria não encontrada no id: {id}')

    return centro_treinamento
