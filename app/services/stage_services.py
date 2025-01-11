from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.database.models.stage import Stage
from app.schemas.stage import StageCreate, StageUpdate


async def get_all_stages(db: AsyncSession):
    """
    Retrieve all stages from the database.

    Args:
        db (AsyncSession): The database session.

    Returns:
        List[Stage]: A list of all stages, or an empty list if an error occurs.
    """
    try:
        query = select(Stage)
        stages = await db.execute(query)
        return stages.scalars().all()
    except SQLAlchemyError as e:
        print(f"Error fetching stages: {e}")
        return []


async def get_stage_by_id(db: AsyncSession, stage_id: int):
    """
    Retrieve a specific stage by its ID.

    Args:
        db (AsyncSession): The database session.
        stage_id (int): The ID of the stage.

    Returns:
        Stage or None: The stage with the given ID, or None if not found or an error occurs.
    """
    try:
        query = select(Stage).where(Stage.id == stage_id)
        stage = await db.execute(query)
        return stage.scalar_one_or_none()
    except SQLAlchemyError as e:
        print(f"Error fetching stage: {e}")
        return None


async def create_stage(db: AsyncSession, stage_data: StageCreate):
    """
    Create a new stage in the database.

    Args:
        db (AsyncSession): The database session.
        stage_data (StageCreate): The data for the new stage.

    Returns:
        Stage or None: The created stage, or None if an error occurs.
    """
    try:
        new_stage = Stage(**stage_data.dict())
        db.add(new_stage)
        await db.commit()
        await db.refresh(new_stage)
        return new_stage
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Error creating stage: {e}")
        return None


async def update_stage(db: AsyncSession, stage_id: int, stage_data: StageUpdate):
    """
    Update an existing stage in the database.

    Args:
        db (AsyncSession): The database session.
        stage_id (int): The ID of the stage to update.
        stage_data (StageUpdate): The updated data for the stage.

    Returns:
        Stage or None: The updated stage, or None if not found or an error occurs.
    """
    try:
        query = select(Stage).where(Stage.id == stage_id)
        stage = await db.execute(query)
        existing_stage = stage.scalar_one_or_none()
        if existing_stage:
            for key, value in stage_data.dict(exclude_unset=True).items():
                setattr(existing_stage, key, value)
            await db.commit()
            await db.refresh(existing_stage)
            return existing_stage
        return None
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Error updating stage: {e}")
        return None


async def delete_stage(db: AsyncSession, stage_id: int):
    """
    Delete a specific stage from the database.

    Args:
        db (AsyncSession): The database session.
        stage_id (int): The ID of the stage to delete.

    Returns:
        bool: True if the stage was deleted, False if not found or an error occurs.
    """
    try:
        query = select(Stage).where(Stage.id == stage_id)
        stage = await db.execute(query)
        existing_stage = stage.scalar_one_or_none()
        if existing_stage:
            await db.delete(existing_stage)
            await db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Error deleting stage: {e}")
        return False