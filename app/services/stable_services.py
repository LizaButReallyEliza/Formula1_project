from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.database.models.stable import Stable
from app.schemas.stable import StableCreate, StableUpdate


async def get_all_stables(db: AsyncSession):
    """
    Retrieve all stables from the database.

    Args:
        db (AsyncSession): The database session.

    Returns:
        List[Stable]: A list of all stables, or an empty list if an error occurs.
    """
    try:
        query = select(Stable)
        stables = await db.execute(query)
        return stables.scalars().all()
    except SQLAlchemyError as e:
        print(f"Error fetching stables: {e}")
        return []


async def get_stable_by_id(db: AsyncSession, stable_id: int):
    """
    Retrieve a specific stable by its ID.

    Args:
        db (AsyncSession): The database session.
        stable_id (int): The ID of the stable.

    Returns:
        Stable or None: The stable with the given ID, or None if not found or an error occurs.
    """
    try:
        query = select(Stable).where(Stable.id == stable_id)
        stable = await db.execute(query)
        return stable.scalar_one_or_none()
    except SQLAlchemyError as e:
        print(f"Error fetching stable: {e}")
        return None


async def create_stable(db: AsyncSession, stable_data: StableCreate):
    """
    Create a new stable in the database.

    Args:
        db (AsyncSession): The database session.
        stable_data (StableCreate): The data for the new stable.

    Returns:
        Stable or None: The created stable, or None if an error occurs.
    """
    try:
        new_stable = Stable(**stable_data.dict())
        db.add(new_stable)
        await db.commit()
        await db.refresh(new_stable)
        return new_stable
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Error creating stable: {e}")
        return None


async def update_stable(db: AsyncSession, stable_id: int, stable_data: StableUpdate):
    """
    Update an existing stable in the database.

    Args:
        db (AsyncSession): The database session.
        stable_id (int): The ID of the stable to update.
        stable_data (StableUpdate): The updated data for the stable.

    Returns:
        Stable or None: The updated stable, or None if not found or an error occurs.
    """
    try:
        query = select(Stable).where(Stable.id == stable_id)
        stable = await db.execute(query)
        existing_stable = stable.scalar_one_or_none()
        if existing_stable:
            for key, value in stable_data.dict(exclude_unset=True).items():
                setattr(existing_stable, key, value)
            await db.commit()
            await db.refresh(existing_stable)
            return existing_stable
        return None
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Error updating stable: {e}")
        return None


async def delete_stable(db: AsyncSession, stable_id: int):
    """
    Delete a specific stable from the database.

    Args:
        db (AsyncSession): The database session.
        stable_id (int): The ID of the stable to delete.

    Returns:
        bool: True if the stable was deleted, False if not found or an error occurs.
    """
    try:
        query = select(Stable).where(Stable.id == stable_id)
        stable = await db.execute(query)
        existing_stable = stable.scalar_one_or_none()
        if existing_stable:
            await db.delete(existing_stable)
            await db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Error deleting stable: {e}")
        return False