from fastapi import APIRouter

from services import DynamoDBService

router = APIRouter()


@router.get('/statistics')
async def statistics():
    return DynamoDBService.get_item()
