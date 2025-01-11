from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database.connection import get_db
from app.schemas.stage import StageCreate, StageRead
from app.database.models.stage import Stage
from app.database.models.result import Result

router = APIRouter()

@router.post("/", status_code=201, response_model=StageRead)
async def create_stage(stage: StageCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new stage.

    Args:
        stage (StageCreate): The data to create a stage.
        db (AsyncSession): The database session.

    Returns:
        StageRead: The created stage data.
    """
    new_stage = Stage(**stage.dict())
    db.add(new_stage)
    await db.commit()
    await db.refresh(new_stage)
    return new_stage

@router.get("/", response_model=list[StageRead])
async def get_stages(db: AsyncSession = Depends(get_db)):
    """
    Retrieve all stages.

    Args:
        db (AsyncSession): The database session.

    Returns:
        List[StageRead]: List of all stages.
    """
    result = await db.execute(select(Stage))
    stages = result.scalars().all()
    return stages

@router.get("/{stage_id}", response_model=StageRead)
async def get_stage(stage_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a stage by its ID.

    Args:
        stage_id (int): The ID of the stage.
        db (AsyncSession): The database session.

    Returns:
        StageRead: The stage with the given ID.

    Raises:
        HTTPException: If the stage with the given ID is not found.
    """
    result = await db.execute(select(Stage).where(Stage.id == stage_id))
    stage = result.scalar_one_or_none()
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    return stage

@router.get("/group_by/")
async def get_average_race_time_per_stage(db: AsyncSession = Depends(get_db)):
    """
    Calculate the average race time for each stage.

    Args:
        db (AsyncSession): The database session.

    Returns:
        List[dict]: List containing stage ID and the corresponding average race time.
    """
    query = (
        select(Result.stage_id, func.avg(Result.race_time).label("avg_race_time"))
        .group_by(Result.stage_id)
    )
    result = await db.execute(query)
    return [{"stage_id": row.stage_id, "avg_race_time": row.avg_race_time} for row in result.all()]