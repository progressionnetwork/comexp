from enum import Enum


class FileType(str, Enum):
    BUILDING = "building"
    INCIDENT = "incident"
    WORK = "work"
    WORK_TYPE_KR = "work_type_kr"
    WORK_TYPE = "work_type"
    EVENT = "event"


model_file_mapper = {
    "Building": {
        "sheet_name": "Sheet1",
        "header_row_num": 0,
    },
    "RoofMaterial": {
        "sheet_name": "COL_781",
        "header_row_num": 1,
    },
    "ProjectSeries": {
        "sheet_name": "COL_758",
        "header_row_num": 1,
    },
    "WallMaterial": {
        "sheet_name": "COL_769",
        "header_row_num": 1,
    },
    "AttributeCrash": {
        "sheet_name": "COL_770",
        "header_row_num": 1,
    },
    "QueueClean": {
        "sheet_name": "COL_775",
        "header_row_num": 1,
    },
    "TypeSocialObject": {
        "sheet_name": "COL_2156",
        "header_row_num": 1,
    },
    "TypeBuildingFund": {
        "sheet_name": "COL_2463",
        "header_row_num": 1,
    },
    "StatusMKD": {
        "sheet_name": "COL_3163",
        "header_row_num": 1,
    },
    "StatusManageMKD": {
        "sheet_name": "COL_3243",
        "header_row_num": 1,
    },
    "CategoryMKD": {
        "sheet_name": "COL_103506",
        "header_row_num": 1,
    },
    "Incident": {
        "sheet_name": ["Result 1", "Result 2"],
        "header_row_num": 0,
    },
    "Work": {
        "sheet_name": None,
        "header_row_num": 0,
    },
    "Event": {
        "sheet_name": None,
        "header_row_num": 0,
    },
    "WorkType": {
        "sheet_name": None,
        "header_row_num": 0,
    },
}

building_df_header_mapper = {
    "COL_756": "year",
    "COL_758": "project_series_id",
    "COL_759": "count_floor",
    "COL_760": "count_entrance",
    "COL_761": "count_apartment",
    "COL_762": "total_area",
    "COL_763": "total_living_area",
    "COL_764": "total_nonliving_area",
    "COL_769": "wall_material_id",
    "COL_770": "attribute_crash_id",
    "COL_771": "count_elevator_passenger",
    "COL_772": "count_elevator_cargopassenger",
    "COL_775": "queue_clean_id",
    "COL_781": "roof_material_id",
    "COL_782": "id",
    "COL_2156": "type_social_object_id",
    "COL_2463": "type_building_fund_id",
    "COL_3163": "status_mkd_id",
    "COL_3243": "status_manage_mkd_id",
    "COL_3363": "count_elevator_cargo",
    "COL_103506": "category_mkd_id",
}

incident_df_header_mapper = {
    "Наименование": "name",
    "Источник": "source",
    "Дата создания во внешней системе": "date_system_create",
    "Дата и время завершения события во": "date_system_close",
    "Дата закрытия": "date_close",
    "unom": "building_id",
}

work_df_header_mapper = {
    "global_id": "id",
    "WORK_NAME": "name",
    "ElevatorNumber": "num_elevator",
    "UNOM": "building_id",
}

event_df_header_mapper = {
    "system": "source_id",
}

work_type_df_header_mapper = {"ID": "id", "NAME": "name"}
work_type_kr_df_header_mapper = {"Код": "id", "Наименование": "name"}

work_date_field = [
    "plan_date_start",
    "plan_date_end",
    "fact_date_start",
    "fact_date_end",
]
