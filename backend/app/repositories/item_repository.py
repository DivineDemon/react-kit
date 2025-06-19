from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.item import Item #type: ignore
from app.schemas.item import ItemCreate, ItemUpdate #type: ignore

class ItemRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self) -> List[Item]:
        result = await self.session.execute(select(Item))
        return result.scalars().all() #type: ignore

    async def get(self, idx: int) -> Optional[Item]:
        return await self.session.get(Item, idx)

    async def create(self, obj_in: ItemCreate) -> Item:
        obj = Item(**obj_in.dict())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, db_obj: Item, obj_in: ItemUpdate) -> Item:
        for field, value in obj_in.dict().items():
            setattr(db_obj, field, value)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, db_obj: Item) -> None:
        await self.session.delete(db_obj)
        await self.session.commit()