from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.connection import get_db
from app.database.models.result import Result
from app.database.models.stable import Stable
from app.database.models.stage import Stage
from app.schemas.result import ResultCreate, ResultRead

router = APIRouter()

@router.post("/", response_model=ResultRead)
async def create_result(result: ResultCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new race result.
    
    Checks if the provided `stable_id` and `stage_id` exist in the database before creating the result.
    
    Args:
        result (ResultCreate): The result data to create.
        db (AsyncSession): The database session.
    
    Returns:
        ResultRead: The created result.
    """
    stable_check = await db.execute(select(Stable).where(Stable.id == result.stable_id))
    if not stable_check.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Invalid stable_id: does not exist")

    stage_check = await db.execute(select(Stage).where(Stage.id == result.stage_id))
    if not stage_check.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Invalid stage_id: does not exist")

    new_result = Result(**result.dict())
    db.add(new_result)
    await db.commit()
    await db.refresh(new_result)
    return new_result

@router.get("/", response_model=list[ResultRead])
async def get_results(db: AsyncSession = Depends(get_db)):
    """
    Get all race results.
    
    Args:
        db (AsyncSession): The database session.
    
    Returns:
        List[ResultRead]: List of all results.
    """
    result = await db.execute(select(Result))
    results = result.scalars().all()
    return results

@router.get("/{result_id}", response_model=ResultRead)
async def get_result(result_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a single race result by ID.
    
    Args:
        result_id (int): The ID of the result.
        db (AsyncSession): The database session.
    
    Returns:
        ResultRead: The result with the specified ID.
    """
    result = await db.execute(select(Result).where(Result.id == result_id))
    result_obj = result.scalar_one_or_none()
    if not result_obj:
        raise HTTPException(status_code=404, detail="Result not found")
    return result_obj

@router.get("/filter/", response_model=list[ResultRead])
async def get_filtered_results(stage_id: int, stable_id: int, db: AsyncSession = Depends(get_db)):
    """
    Filter results by `stage_id` and `stable_id`.
    
    Args:
        stage_id (int): The ID of the stage to filter by.
        stable_id (int): The ID of the stable to filter by.
        db (AsyncSession): The database session.
    
    Returns:
        List[ResultRead]: List of filtered results.
    """
    result = await db.execute(
        select(Result).where(Result.stage_id == stage_id, Result.stable_id == stable_id)
    )
    results = result.scalars().all()
    return results

@router.get("/join/", response_model=list[dict])
async def get_results_with_details(db: AsyncSession = Depends(get_db)):
    """
    Get results with stage and stable details.
    
    Performs a JOIN operation to include `stage_name` and `stable_name` in the results.
    
    Args:
        db (AsyncSession): The database session.
    
    Returns:
        List[dict]: List of results with additional details.
    """
    query = (
        select(Result, Stage.name.label("stage_name"), Stable.name.label("stable_name"))
        .join(Stage, Result.stage_id == Stage.id)
        .join(Stable, Result.stable_id == Stable.id)
    )
    result = await db.execute(query)
    results = [
        {
            "id": row.Result.id,
            "driver_name": row.Result.driver_name,
            "race_time": row.Result.race_time,
            "stage_name": row.stage_name,
            "stable_name": row.stable_name,
        }
        for row in result.all()
    ]
    return results

@router.put("/update_laps/")
async def update_laps(race_time_threshold: float, new_laps: int, db: AsyncSession = Depends(get_db)):
    """
    Update the number of laps for results where the race time exceeds a threshold.
    
    Args:
        race_time_threshold (float): The race time threshold to filter by.
        new_laps (int): The new number of laps to set.
        db (AsyncSession): The database session.
    
    Returns:
        dict: A message indicating the number of updated records.
    """
    result = await db.execute(
        select(Result).where(Result.race_time > race_time_threshold)
    )
    results_to_update = result.scalars().all()

    for result in results_to_update:
        result.laps = new_laps

    await db.commit()
    return {"message": f"{len(results_to_update)} results updated."}

@router.get("/sorted/", response_model=list[ResultRead])
async def get_sorted_results(order: str = "asc", db: AsyncSession = Depends(get_db)):
    """
    Get results sorted by `race_time`.
    
    Args:
        order (str): The sort order, either "asc" (ascending) or "desc" (descending).
        db (AsyncSession): The database session.
    
    Returns:
        List[ResultRead]: List of sorted results.
    """
    if order.lower() == "asc":
        query = select(Result).order_by(Result.race_time.asc())
    elif order.lower() == "desc":
        query = select(Result).order_by(Result.race_time.desc())
    else:
        raise HTTPException(status_code=400, detail="Invalid order parameter. Use 'asc' or 'desc'.")

    result = await db.execute(query)
    results = result.scalars().all()
    return results