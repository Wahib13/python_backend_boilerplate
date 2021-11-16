"""
OMCs are Oil Marketing Companies
"""
from typing import List

from fastapi import APIRouter, Depends

from dependencies.auth import get_current_user
from dependencies.data import query_omcs, query_omc, query_create_omc
from models import OMCInDB, User

router = APIRouter(
    prefix='/omcs',
    tags=['OMCs']
)


@router.get("/", response_model=List[OMCInDB])
def get_omcs(omcs: List[OMCInDB] = Depends(query_omcs), user: User = Depends(get_current_user)):
    return omcs


@router.get("/{id}")
def get_omc(omc: OMCInDB = Depends(query_omc)):
    return omc


@router.post("/", response_model=OMCInDB)
def create_omc(omc: OMCInDB = Depends(query_create_omc), user: User = Depends(get_current_user)):
    return omc
