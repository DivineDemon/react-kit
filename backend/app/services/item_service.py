from typing import List
from app.repositories.item_repository import ItemRepository #type: ignore
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate #type: ignore
from sqlalchemy.ext.asyncio import AsyncSession

class ItemService:
    def __init__(self, session: AsyncSession):
        self.repo = ItemRepository(session)

    async def list_items(self) -> List[ItemRead]:
        items = await self.repo.list()
        return [ItemRead.from_orm(i) for i in items]

    async def get_item(self, id: int) -> ItemRead:
        item = await self.repo.get(id)
        return ItemRead.from_orm(item)

    async def create_item(self, data: ItemCreate) -> ItemRead:
        item = await self.repo.create(data)
        return ItemRead.from_orm(item)

    async def update_item(self, id: int, data: ItemUpdate) -> ItemRead:
        db_obj = await self.repo.get(id)
        updated = await self.repo.update(db_obj, data)
        return ItemRead.from_orm(updated)

    async def delete_item(self, id: int) -> None:
        db_obj = await self.repo.get(id)
        await self.repo.delete(db_obj)