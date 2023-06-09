from building.models import (
    AttributeCrash,
    AttributeCrashBase,
    Building,
    BuildingBase,
    BuildingMinimal,
    BuildingMinimalRead,
    BuildingRead,
    CategoryMKD,
    CategoryMKDBase,
    ProjectSeries,
    ProjectSeriesBase,
    QueueClean,
    QueueCleanBase,
    RoofMaterial,
    RoofMaterialBase,
    StatusManageMKD,
    StatusManageMKDBase,
    StatusMKD,
    StatusMKDBase,
    TypeBuildingFund,
    TypeBuildingFundBase,
    TypeSocialObject,
    TypeSocialObjectBase,
    WallMaterial,
    WallMaterialBase,
)
from fastapi import Depends
from share.database import get_session
from share.exceptions import UnkownModelError
from share.routers import CRUDRouter
from share.utils import pagination
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

router_category_mkd = CRUDRouter(
    create_model=CategoryMKDBase, read_model=CategoryMKD, update_model=CategoryMKDBase, db_model=CategoryMKD
)
router_status_manage_mkd = CRUDRouter(
    create_model=StatusManageMKDBase,
    read_model=StatusManageMKD,
    update_model=StatusManageMKDBase,
    db_model=StatusManageMKD,
)
router_status_mkd = CRUDRouter(
    create_model=StatusMKDBase, read_model=StatusMKD, update_model=StatusMKDBase, db_model=StatusMKD
)

router_type_building = CRUDRouter(
    create_model=TypeBuildingFundBase,
    read_model=TypeBuildingFund,
    update_model=TypeBuildingFundBase,
    db_model=TypeBuildingFund,
)


router_type_social = CRUDRouter(
    create_model=TypeSocialObjectBase,
    read_model=TypeSocialObject,
    update_model=TypeSocialObjectBase,
    db_model=TypeSocialObject,
)


router_queue_clean = CRUDRouter(
    create_model=QueueCleanBase,
    read_model=QueueClean,
    update_model=QueueCleanBase,
    db_model=QueueClean,
)


router_attribute_crash = CRUDRouter(
    create_model=AttributeCrashBase,
    read_model=AttributeCrash,
    update_model=AttributeCrashBase,
    db_model=AttributeCrash,
)

router_wall_material = CRUDRouter(
    create_model=WallMaterialBase,
    read_model=WallMaterial,
    update_model=WallMaterialBase,
    db_model=WallMaterial,
)

router_roof_material = CRUDRouter(
    create_model=RoofMaterialBase,
    read_model=RoofMaterial,
    update_model=RoofMaterialBase,
    db_model=RoofMaterial,
)

router_project_series = CRUDRouter(
    create_model=ProjectSeriesBase,
    read_model=ProjectSeries,
    update_model=ProjectSeriesBase,
    db_model=ProjectSeries,
)

router_building = CRUDRouter(
    create_model=BuildingBase,
    read_model=BuildingRead,
    update_model=BuildingBase,
    db_model=Building,
)


@router_building.get("/minimal/", response_model=list[BuildingMinimalRead], response_model_exclude_none=True)
async def get_all_minimal(
    pagination: dict = Depends(pagination),
    session: AsyncSession = Depends(get_session),
    # current_user=Depends(get_current_user_with_permmissions(model="OKPD2", type_permissions="read")),
):
    try:
        statement = select(BuildingMinimal).limit(pagination.get("limit"))
        result = await session.execute(statement)
    except Exception as error:
        raise UnkownModelError(model="Building", msg=str(error))
    return result.scalars().all()
