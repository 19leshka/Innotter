from fastapi import APIRouter
from pydantic import BaseModel

from services import DynamoDBService

router = APIRouter()


class Item(BaseModel):
    id: int
    total_followers: int
    total_posts: int
    total_likes: int


@router.get('/statistics/{page_id}', response_model=Item)
async def statistics(item_id: int) -> dict:
    item = DynamoDBService.get_item(item_id)['Item']
    return {**item}

