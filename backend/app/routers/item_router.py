from fastapi import APIRouter, Depends, HTTPException, status
from app.db.session import async_session #type: ignore
from app.services.item_service import ItemService #type: ignore
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate #type: ignore

router = APIRouter()

def get_service():
    async def _get():
        async with async_session() as session:
            yield ItemService(session)
    return _get

@router.get("/", response_model=list[ItemRead]) #type: ignore
async def list_items(service: ItemService = Depends(get_service())):
    return await service.list_items()

@router.get("/{id}", response_model=ItemRead)
async def get_item(id: int, service: ItemService = Depends(get_service())):
    try:
        return await service.get_item(id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(data: ItemCreate, service: ItemService = Depends(get_service())):
    return await service.create_item(data)

@router.put("/{id}", response_model=ItemRead)
async def update_item(id: int, data: ItemUpdate, service: ItemService = Depends(get_service())):
    return await service.update_item(id, data)

@router.delete("/{id}")
async def delete_item(id: int, service: ItemService = Depends(get_service())):
    await service.delete_item(id)
    return {"ok": True}