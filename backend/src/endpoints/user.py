from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from pydantic.main import BaseModel
from sqlalchemy.orm import Session
from src.database import session_for_request
from src.database.user import get_user_by_id
from src.database.user import get_user_missions_by_wallet
from src.endpoints.constants import USER_TAG
from src.models.users import UserSchema

router = APIRouter()


class UserRequest(BaseModel):
    id: int


class UserResponse(BaseModel):
    result: bool
    user: Optional[UserSchema]


class MissionsResponse(BaseModel):
    missions: List[int]


@router.get('/user/{user_id}', tags=[USER_TAG], response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(session_for_request)):
    res, user = get_user_by_id(db, user_id)
    if res:
        return {'result': True, 'user': {'totalPoints': user.total_points, 'wallet': user.wallet}}
    else:
        return {'result': False}


@router.get('/user_missions/{user_wallet}', tags=[USER_TAG], response_model=MissionsResponse)
async def get_user_missions(user_wallet: str, db: Session = Depends(session_for_request)):
    res, missions = get_user_missions_by_wallet(db, user_wallet)
    if not res:
        missions = []
    return {'missions': missions}
