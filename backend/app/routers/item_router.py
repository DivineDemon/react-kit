from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants.utils import get_current_user
from app.core.db import get_db
from app.models.item import Item as ORMItem
from app.schemas.generic import ResponseModel
from app.schemas.item_schema import ItemBase, ItemDelete, ItemRead, ItemUpdate

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=ResponseModel[ItemRead])
async def create_item(
    item: ItemBase,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        new_item = ORMItem(
            name=item.name,
            description=item.description,
            image_url=str(item.image_url),
            owner_id=current_user.user_id
        )

        db.add(new_item)
        await db.commit()
        await db.refresh(new_item)

        return ResponseModel(
            status=status.HTTP_201_CREATED,
            data=ItemRead.model_validate(new_item),
            message="Item Created Successfully"
        )
    except Exception as e:
        await db.rollback()
        return ResponseModel(
            data=None,
            message=str(e),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get("/", response_model=ResponseModel[list[ItemRead]])
async def get_items(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        result = await db.execute(select(ORMItem).
                                  where(ORMItem.owner_id == current_user.user_id))
        items = result.scalars().all()

        if not items:
            return ResponseModel(
                data=None,
                message="No Items Found",
                status=status.HTTP_404_NOT_FOUND
            )

        return ResponseModel(
            status=status.HTTP_200_OK,
            message="Items Retrieved Successfully",
            data=[ItemRead.model_validate(i) for i in items]
        )
    except Exception as e:
        return ResponseModel(
            data=None,
            message=str(e),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get("/{item_id}", response_model=ResponseModel[ItemRead])
async def get_item(
    item_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(select(ORMItem).where(ORMItem.id == item_id))
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


@router.put("/{item_id}", response_model=ResponseModel[ItemRead])
async def update_item(
    item_id: int,
    item: ItemUpdate,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(select(ORMItem).where(ORMItem.id == item_id))
        db_item = result.scalar_one_or_none()

        if not db_item:
            return ResponseModel(
                data=None,
                message="Item Not Found",
                status=status.HTTP_404_NOT_FOUND
            )

        for k, v in item.model_dump(exclude_unset=True).items():
            setattr(db_item, k, str(v) if k ==
                    "image_url" and v is not None else v)

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


@router.delete("/{item_id}", response_model=ResponseModel[ItemDelete])
async def delete_item(
    item_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(select(ORMItem).where(ORMItem.id == item_id))
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
