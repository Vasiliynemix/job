import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr, constr


class TunedModel(BaseModel):
    class Config:
        orm_mode = True


class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


class CreateUser(BaseModel):
    name: str
    surname: str
    email: EmailStr

    # @validator('name')
    # def validator_name(cls, value):
    #     return True
    #
    # @validator('surname')
    # def validator_name(cls, value):
    #     return True


class DeleteUserResponse(BaseModel):
    deleted_user_id: uuid.UUID


class UpdatedUserResponse(BaseModel):
    updated_user_id: uuid.UUID


class UpdateUserRequest(BaseModel):
    name: Optional[constr(min_length=1)]
    surname: Optional[constr(min_length=1)]
    email: Optional[EmailStr]
