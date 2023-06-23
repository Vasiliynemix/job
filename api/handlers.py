from logging import getLogger
from typing import Union
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import CreateUser, ShowUser, DeleteUserResponse, UpdateUserRequest, UpdatedUserResponse
from db.base_logic import UserLogic
from db.session import get_db

logger = getLogger(__name__)

router_user = APIRouter()


async def _create_new_user(body: CreateUser, db) -> ShowUser:
    async with db as session:
        async with session.begin():
            user_logic = UserLogic(session)
            user = await user_logic.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email
            )
            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active
            )


async def _delete_user(user_id: str, db) -> Union[UUID, None]:
    async with db as session:
        async with session.begin():
            user_logic = UserLogic(session)
            deleted_user_id = await user_logic.delete_user(user_id=user_id)
            return deleted_user_id


async def _update_user(updated_user_params: dict, user_id: UUID, db) -> Union[UUID, None]:
    async with db as session:
        async with session.begin():
            user_dal = UserLogic(session)
            updated_user_id = await user_dal.update_user(
                user_id=user_id,
                **updated_user_params
            )
            return updated_user_id


async def _get_user_by_id(user_id, db) -> Union[ShowUser, None]:
    async with db as session:
        async with session.begin():
            user_logic = UserLogic(session)
            user = await user_logic.get_user_by_id(user_id=user_id)
            if user is not None:
                return ShowUser(
                    user_id=user.user_id,
                    name=user.name,
                    surname=user.surname,
                    email=user.email,
                    is_active=user.is_active
                )


@router_user.post('/', response_model=ShowUser)
async def create_user(body: CreateUser, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as error:
        logger.error(error)
        raise HTTPException(status_code=503, detail=f'Database error: {error}')


@router_user.delete('/', response_model=DeleteUserResponse)
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)) -> DeleteUserResponse:
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(status_code=404, detail=f'User with id {user_id} not found.')
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@router_user.get('/', response_model=ShowUser)
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db)) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f'User with {user_id} not found.')
    return user


@router_user.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
        user_id: UUID, body: UpdateUserRequest, db: AsyncSession = Depends(get_db)
) -> UpdatedUserResponse:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(status_code=422, detail="At least one parameter for user update info should be provided")
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found.")
    try:
        updated_user_id = await _update_user(updated_user_params=updated_user_params, db=db, user_id=user_id)
    except IntegrityError as error:
        logger.error(error)
        raise HTTPException(status_code=503, detail=f'Database error: {error}')
    return UpdatedUserResponse(updated_user_id=updated_user_id)
