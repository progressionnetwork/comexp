from sqlmodel import Field, Relationship, SQLModel


class CategoryMKDBase(SQLModel):
    name: str | None


class CategoryMKD(CategoryMKDBase, table=True):
    # COL_103506
    id: int = Field(primary_key=True, index=True, default=None)


class StatusManageMKDBase(SQLModel):
    name: str | None


class StatusManageMKD(StatusManageMKDBase, table=True):
    # COL_3243
    id: int = Field(primary_key=True, index=True, default=None)


class StatusMKDBase(SQLModel):
    name: str | None


class StatusMKD(StatusMKDBase, table=True):
    # COL_3163
    id: int = Field(primary_key=True, index=True, default=None)


class TypeBuildingFundBase(SQLModel):
    name: str | None


class TypeBuildingFund(TypeBuildingFundBase, table=True):
    # COL_2463
    id: int = Field(primary_key=True, index=True, default=None)


class TypeSocialObjectBase(SQLModel):
    name: str | None


class TypeSocialObject(TypeSocialObjectBase, table=True):
    # COL_2156
    id: int = Field(primary_key=True, index=True, default=None)


class QueueCleanBase(SQLModel):
    name: str | None


class QueueClean(QueueCleanBase, table=True):
    # COL_775
    id: int = Field(primary_key=True, index=True, default=None)


class AttributeCrashBase(SQLModel):
    name: str | None


class AttributeCrash(AttributeCrashBase, table=True):
    # COL_770
    id: int = Field(primary_key=True, index=True, default=None)


class WallMaterialBase(SQLModel):
    name: str | None


class WallMaterial(WallMaterialBase, table=True):
    # COL_769
    id: int = Field(primary_key=True, index=True, default=None)


class ProjectSeriesBase(SQLModel):
    name: str | None


class ProjectSeries(ProjectSeriesBase, table=True):
    # COL_758
    id: int = Field(primary_key=True, index=True, default=None)


class RoofMaterialBase(SQLModel):
    name: str | None


class RoofMaterial(RoofMaterialBase, table=True):
    # COL_781
    id: int = Field(primary_key=True, index=True, default=None)


class BuildingBase(SQLModel):
    name: str
    login: str = ""
    year: int = 0
    count_floor: int = 0
    count_entrance: int = 0
    count_apartment: int = 0
    count_elevator_passenger: int = 0
    count_elevator_cargopassenger: int = 0
    count_elevator_cargo: int = 0
    total_area: int = 0
    total_living_area: int = 0
    total_nonliving_area: int = 0

    unom: int


class Building(BuildingBase, table=True):
    id: int = Field(primary_key=True, index=True, default=None)

    project_series_id: int | None = Field(default=None, foreign_key="projectseries.id")
    project_series: ProjectSeries = Relationship(sa_relationship_kwargs={"lazy": "selectin"})

    wall_material_id: int | None = Field(default=None, foreign_key="wallmaterial.id")
    wall_material: WallMaterial = Relationship(sa_relationship_kwargs={"lazy": "selectin"})

    attribute_crash_id: int | None = Field(default=None, foreign_key="attributecrash.id")
    attribute_crash: AttributeCrash = Relationship(sa_relationship_kwargs={"lazy": "selectin"})

    queue_clean_id: int | None = Field(default=None, foreign_key="queueclean.id")
    queue_clean: QueueClean = Relationship(sa_relationship_kwargs={"lazy": "selectin"})

    roof_material_id: int | None = Field(default=None, foreign_key="roofmaterial.id")
    roof_material: RoofMaterial = Relationship(sa_relationship_kwargs={"lazy": "selectin"})

    type_building_fund_id: int | None = Field(default=None, foreign_key="typebuildingfund.id")
    type_building_fund: TypeBuildingFund = Relationship(sa_relationship_kwargs={"lazy": "selectin"})

    status_mkd_id: int | None = Field(default=None, foreign_key="statusmkd.id")
    status_mkd: StatusMKD = Relationship(sa_relationship_kwargs={"lazy": "selectin"})

    status_manage_mkd_id: int | None = Field(default=None, foreign_key="statusmanagemkd.id")
    status_manage_mkd: StatusManageMKD = Relationship(sa_relationship_kwargs={"lazy": "selectin"})
