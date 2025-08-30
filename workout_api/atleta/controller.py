from ast import List
from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, status, HTTPException
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaIn, AtletaOut
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel


router = APIRouter()


@router.post(
    "/",
    summary="Criar um novo atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)):

    try:
        categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome))).scalars().first()

        if not categoria:
            print('fakeee')

        centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=atleta_in.centro_treinamento.nome))).scalars().first()

        if not categoria:
            print('fakeee')

        atleta_model = AtletaModel(
            nome=atleta_in.nome,
            cpf=atleta_in.cpf,
            idade=atleta_in.idade,
            altura=atleta_in.altura,
            peso=atleta_in.peso,
            sexo=atleta_in.sexo,
            categoria=categoria,
            categoria_id=categoria.pk_id,
            centro_treinamento=centro_treinamento,
            centro_treinamento_id=centro_treinamento.pk_id
        )

        db_session.add(atleta_model)
        await db_session.commit()
        await db_session.refresh(atleta_model)

        atleta_out = AtletaOut(
            id=uuid4(),
            nome=atleta_model.nome,
            cpf=atleta_model.cpf,
            idade=atleta_model.idade,
            peso=atleta_model.peso,
            sexo=atleta_model.sexo,
        )

        return atleta_out
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atleta: {str(e)}",
        )


@router.get('/', summary="Consultar todos os centro de treinamentos", status_code=status.HTTP_200_OK, response_model=list[AtletaOut],)
async def get(db_session: DatabaseDependency) -> list[AtletaOut]:

    query = select(AtletaModel).options(
        selectinload(AtletaModel.categoria),
        selectinload(AtletaModel.centro_treinamento)
    )
 
    result = await db_session.execute(query)
    
    atletas: List[AtletaModel] = result.scalars().all()

    return atletas


@router.get('/{id}', summary="Consultar atleta por id", status_code=status.HTTP_200_OK, response_model=AtletaOut,)
async def get_by_id(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:

    query = select(AtletaModel).options(
        selectinload(AtletaModel.categoria),
        selectinload(AtletaModel.centro_treinamento)
    ).filter_by(id=id)
 
    result = await db_session.execute(query)
    
    atleta: AtletaModel = result.scalars().first()

    return atleta