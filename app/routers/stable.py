from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.connection import get_db
from app.database.models.stable import Stable
from app.schemas.stable import StableCreate, StableRead

router = APIRouter()

@router.post("/", response_model=StableRead)
async def create_stable(stable: StableCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new stable.

    Args:
        stable (StableCreate): The data to create a stable.
        db (AsyncSession): The database session.

    Returns:
        StableRead: The created stable data.
    """
    new_stable = Stable(**stable.dict())
    db.add(new_stable)
    await db.commit()
    await db.refresh(new_stable)
    return new_stable

@router.get("/", response_model=list[StableRead])
async def get_stables(db: AsyncSession = Depends(get_db)):
    """
    Retrieve all stables.

    Args:
        db (AsyncSession): The database session.

    Returns:
        List[StableRead]: List of all stables.
    """
    result = await db.execute(select(Stable))
    stables = result.scalars().all()
    return stables

@router.get("/{stable_id}", response_model=StableRead)
async def get_stable(stable_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a stable by its ID.

    Args:
        stable_id (int): The ID of the stable.
        db (AsyncSession): The database session.

    Returns:
        StableRead: The stable with the given ID.

    Raises:
        HTTPException: If the stable with the given ID is not found.
    """
    result = await db.execute(select(Stable).where(Stable.id == stable_id))
    stable = result.scalar_one_or_none()
    if not stable:
        raise HTTPException(status_code=404, detail="Stable not found")
    return stable