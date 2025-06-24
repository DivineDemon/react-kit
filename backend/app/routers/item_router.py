from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.item import Item as ORMItem
from app.schemas.generic import ResponseModel
from app.schemas.item_schema import ItemBase, ItemDelete, ItemRead, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/")
async def create_item(item: ItemBase, db: AsyncSession = \
                       Depends(get_db)) -> ResponseModel[ItemRead]:
    try:
        item = ORMItem(
            name=item.name,
            description=item.description,
            image_url=str(item.image_url)
        )

        db.add(item)
        await db.commit()
        await db.refresh(item)

        return ResponseModel(
            status=status.HTTP_201_CREATED,
            data=ItemRead.model_validate(item),
            message="Item Created Successfully"
        )
    except Exception as e:
        await db.rollback()

        return ResponseModel(
            data=None,
            message=str(e),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get("/")
async def get_items(db: AsyncSession = \
                     Depends(get_db)) -> ResponseModel[list[ItemRead]]:
    try:
        query = select(ORMItem)
        results = await db.execute(query)
        items = results.scalars().all()

        if not items:
            return ResponseModel(
                data=None,
                message="No Items Found",
                status=status.HTTP_404_NOT_FOUND
            )

        return ResponseModel(
            status=status.HTTP_200_OK,
            message="Items Retrieved Successfully",
            data=[ItemRead.model_validate(item) for item in items]
        )
    except Exception as e:
        return ResponseModel(
            data=None,
            message=str(e),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get("/{item_id}")
async def get_item(item_id: int, db: AsyncSession = \
                    Depends(get_db)) -> ResponseModel[ItemRead]:
    try:
        query = select(ORMItem).where(ORMItem.id == item_id)
        result = await db.execute(query)
        item = result.scalar_one_or_none()

        if not item:
            return ResponseModel(
                data=None,
                message="Item Not Found",
                status=status.HTTP_404_NOT_FOUND
            )

        return ResponseModel(
            status=status.HTTP_200_OK,
            data=ItemRead.model_validate(item),
            message="Item Retrieved Successfully"
        )
    except Exception as e:
        return ResponseModel(
            data=None,
            message=str(e),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.put("/{item_id}")
async def update_item(item_id: int, item: ItemUpdate, db: AsyncSession = \
                       Depends(get_db)) -> ResponseModel[ItemRead]:
    try:
        query = select(ORMItem).where(ORMItem.id == item_id)
        result = await db.execute(query)
        db_item = result.scalar_one_or_none()

        if not db_item:
            return ResponseModel(
                data=None,
                message="Item Not Found",
                status=status.HTTP_404_NOT_FOUND
            )

        for key, value in item.model_dump(exclude_unset=True).items():
            if key == "image_url" and value is not None:
                setattr(db_item, key, str(value))
            else:
                setattr(db_item, key, value)

        await db.commit()
        await db.refresh(db_item)

        return ResponseModel(
            status=status.HTTP_200_OK,
            message="Item Updated Successfully",
            data=ItemRead.model_validate(db_item)
        )
    except Exception as e:
        await db.rollback()

        return ResponseModel(
            data=None,
            message=str(e),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.delete("/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = \
                       Depends(get_db)) -> ResponseModel[ItemDelete]:
    try:
        query = select(ORMItem).where(ORMItem.id == item_id)
        result = await db.execute(query)
        item = result.scalar_one_or_none()

        if not item:
            return ResponseModel(
                data=None,
                message="Item Not Found",
                status=status.HTTP_404_NOT_FOUND
            )

        await db.delete(item)
        await db.commit()

        return ResponseModel(
            status=status.HTTP_200_OK,
            data=ItemDelete(id=item_id),
            message="Item Deleted Successfully"
        )
    except Exception as e:
        await db.rollback()

        return ResponseModel(
            data=None,
            message=str(e),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
