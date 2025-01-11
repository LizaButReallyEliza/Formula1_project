from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.database.models.result import Result
from app.schemas.result import ResultCreate, ResultUpdate


async def get_all_results(db: AsyncSession):
    """
    Retrieve all results from the database.

    Args:
        db (AsyncSession): The database session.

    Returns:
        List[Result]: A list of all results, or an empty list if an error occurs.
    """
    try:
        query = select(Result)
        results = await db.execute(query)
        return results.scalars().all()
    except SQLAlchemyError as e:
        print(f"Error fetching results: {e}")
        return []


async def get_result_by_id(db: AsyncSession, result_id: int):
    """
    Retrieve a specific result by its ID.

    Args:
        db (AsyncSession): The database session.
        result_id (int): The ID of the result.

    Returns:
        Result or None: The result with the given ID, or None if not found or an error occurs.
    """
    try:
        query = select(Result).where(Result.id == result_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        print(f"Error fetching result: {e}")
        return None


async def create_result(db: AsyncSession, result_data: ResultCreate):
    """
    Create a new result in the database.

    Args:
        db (AsyncSession): The database session.
        result_data (ResultCreate): The data for the new result.

    Returns:
        Result or None: The created result, or None if an error occurs.
    """
    try:
        new_result = Result(**result_data.dict())
        db.add(new_result)
        await db.commit()
        await db.refresh(new_result)
        return new_result
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Error creating result: {e}")
        return None


async def update_result(db: AsyncSession, result_id: int, result_data: ResultUpdate):
    """
    Update an existing result in the database.

    Args:
        db (AsyncSession): The database session.
        result_id (int): The ID of the result to update.
        result_data (ResultUpdate): The updated data for the result.

    Returns:
        Result or None: The updated result, or None if not found or an error occurs.
    """
    try:
        query = select(Result).where(Result.id == result_id)
        result = await db.execute(query)
        existing_result = result.scalar_one_or_none()
        if existing_result:
            for key, value in result_data.dict(exclude_unset=True).items():
                setattr(existing_result, key, value)
            await db.commit()
            await db.refresh(existing_result)
            return existing_result
        return None
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Error updating result: {e}")
        return None


async def delete_result(db: AsyncSession, result_id: int):
    """
    Delete a specific result from the database.

    Args:
        db (AsyncSession): The database session.
        result_id (int): The ID of the result to delete.

    Returns:
        bool: True if the result was deleted, False if not found or an error occurs.
    """
    try:
        query = select(Result).where(Result.id == result_id)
        result = await db.execute(query)
        existing_result = result.scalar_one_or_none()
        if existing_result:
            await db.delete(existing_result)
            await db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"Error deleting result: {e}")
        return False