from typing import Union
from uuid import UUID

from api.models import CreateUser
from api.models import ShowUser
from db.base_logic import PortalRole
from db.base_logic import UserLogic
from db.models import User
from hashing import Hasher


async def _create_new_user(body: CreateUser, session) -> ShowUser:
    async with session.begin():
        user_logic = UserLogic(session)
        user = await user_logic.create_user(
            name=body.name,
            surname=body.surname,
            email=body.email,
            hashed_password=Hasher.get_password_hash(body.password),
            roles=[
                PortalRole.ROLE_PORTAL_USER,
            ],
        )
        return ShowUser(
            user_id=user.user_id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            is_active=user.is_active,
        )


async def _delete_user(user_id: str, session) -> Union[UUID, None]:
    async with session.begin():
        user_logic = UserLogic(session)
        deleted_user_id = await user_logic.delete_user(user_id=user_id)
        return deleted_user_id


async def _update_user(
    updated_user_params: dict, user_id: UUID, session
) -> Union[UUID, None]:
    async with session.begin():
        user_dal = UserLogic(session)
        updated_user_id = await user_dal.update_user(
            user_id=user_id, **updated_user_params
        )
        return updated_user_id


async def _get_user_by_id(user_id, session) -> Union[User, None]:
    async with session.begin():
        user_logic = UserLogic(session)
        user = await user_logic.get_user_by_id(user_id=user_id)
        if user is not None:
            return user


def check_user_permission(target_user: User, current_user: User) -> bool:
    if (
        target_user.user_id == current_user.user_id
        and PortalRole.ROLE_PORTAL_SUPERADMIN in current_user.roles
    ):
        return False
    if target_user.user_id != current_user.user_id:
        # check admin role
        if not {
            PortalRole.ROLE_PORTAL_ADMIN,
            PortalRole.ROLE_PORTAL_SUPERADMIN,
        }.intersection(current_user.roles):
            return False
        # check admin deactivate superadmin
        if (
            PortalRole.ROLE_PORTAL_SUPERADMIN in target_user.roles
            and PortalRole.ROLE_PORTAL_ADMIN in current_user.roles
        ):
            return False
        # check admin deactivate admin
        if (
            PortalRole.ROLE_PORTAL_ADMIN in target_user.roles
            and PortalRole.ROLE_PORTAL_ADMIN in current_user.roles
        ):
            return False
    return True
