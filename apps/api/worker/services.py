import uuid
from datetime import datetime
from typing import Callable

import numpy as np
import pandas as pd
from building.models import (
    AttributeCrash,
    Building,
    CategoryMKD,
    ProjectSeries,
    QueueClean,
    RoofMaterial,
    StatusManageMKD,
    StatusMKD,
    TypeBuildingFund,
    TypeSocialObject,
    WallMaterial,
)
from event.models import Event, SourceSystem
from files.constants import (
    FileType,
    building_df_header_mapper,
    event_df_header_mapper,
    incident_df_header_mapper,
    model_file_mapper,
    work_date_field,
    work_df_header_mapper,
    work_type_df_header_mapper,
    work_type_kr_df_header_mapper,
)
from files.models import FileData
from incident.models import Incident
from plan.models import Plan, PlanEvent, PlanRead, PlanWork
from plan.predict.predict import get_incident, get_works
from share.database_sync import get_session
from share.services import get_one
from share.utils import list_chunk
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only
from sqlmodel import SQLModel, col, func, select
from work.models import Work, WorkType


def __get_or_create_instance(db_model, expressions: list, default_value: dict):
    session = get_session().__next__()
    statement = select(db_model).where(*expressions)
    resutls = session.exec(statement)
    try:
        instance = resutls.one_or_none()
    except MultipleResultsFound:
        resutls = session.exec(statement)
        instance = resutls.first()
    if instance is None:
        instance = db_model(**default_value)
        session.add(instance)
        session.commit()
        session.refresh(instance)
    session.close()
    return instance


def _presave_building(df: pd.DataFrame) -> pd.DataFrame:
    df["name"] = df["name"].apply(lambda x: str(x).replace("Дом по адресу ", ""))
    df = df.dropna(subset=["name"])
    return df


def _presave_event(df: pd.DataFrame) -> pd.DataFrame:
    df["source_id"] = df["source_id"].apply(
        lambda system_source: __get_or_create_instance(
            db_model=SourceSystem,
            expressions=[SourceSystem.name == system_source],
            default_value={"name": system_source},
        ).id
    )
    df["id"] = df["id"].apply(lambda system_id: int(uuid.UUID(system_id).hex[:6], 16))
    return df


def _presave_incident(df: pd.DataFrame) -> pd.DataFrame:
    def update_source(df_row, all_sources: list):
        source = str(df_row["source"])
        filter_source = list(filter(lambda row: source == row.get("name"), all_sources))
        if len(filter_source) == 0:
            return np.NaN
        else:
            return filter_source[0].get("id")

    def update_event(df_row, all_events: list):
        source = df_row["source"]
        event_name = df_row["name"]
        filter_event = list(
            filter(lambda row: event_name == row.get("name") and source == row.get("source_id"), all_events)
        )
        if len(filter_event) == 0:
            return np.NaN
        else:
            return filter_event[0].get("id")

    print(f"PRESAVE_INCIDENT: Started")
    session = get_session().__next__()
    statement = select(SourceSystem)
    resutls = session.exec(statement)
    sources = resutls.all()
    list_dict_sources = [source.dict() for source in sources]

    df["source"] = df.apply(
        lambda x: update_source(df_row=x, all_sources=list_dict_sources),
        axis=1,
    )
    print(f"PRESAVE_INCIDENT: Finished source update")
    session = get_session().__next__()
    statement = select(Event)
    resutls = session.exec(statement)
    events = resutls.all()
    list_dict_events = [event.dict() for event in events]

    df["event_id"] = df.apply(
        lambda x: update_event(df_row=x, all_events=list_dict_events),
        axis=1,
    )
    print(f"PRESAVE_INCIDENT: Finished event update")
    session = get_session().__next__()
    statement = select(Building).options(load_only("id"))
    resutls = session.exec(statement)
    buildings = resutls.all()
    buildings_ids = [building.id for building in buildings]
    df = df.loc[df["building_id"].isin(buildings_ids)]
    print(f"PRESAVE_INCIDENT: Finished building_id update")

    df = df.drop("name", axis=1)
    df = df.drop("source", axis=1)
    print(f"PRESAVE_INCIDENT: Finished drop")
    return df


def _presave_worktype(df: pd.DataFrame) -> pd.DataFrame:
    df["is_kr"] = False
    return df[["id", "name", "is_kr"]]


def _presave_worktype_kr(df: pd.DataFrame) -> pd.DataFrame:
    df["is_kr"] = True
    return df[["name", "is_kr"]]


def _presave_work(df: pd.DataFrame) -> pd.DataFrame:
    df["work_type_id"] = df.apply(
        lambda x: __get_or_create_instance(
            db_model=WorkType,
            expressions=[WorkType.name == x["name"]],
            default_value={"name": x["name"], "is_kr": False},
        ).id,
        axis=1,
    )
    df.drop("name", axis=1)
    return df


def _update_model(
    db_model,
    file_path: str,
    df_header_maper: dict | None = None,
    df_date_field: list | None = None,
    presave: Callable[[pd.DataFrame], pd.DataFrame] | None = None,
    offset_header: int = 0,
):
    header = model_file_mapper[db_model.__name__]["header_row_num"]
    sheet_name = model_file_mapper[db_model.__name__]["sheet_name"]

    session = get_session().__next__()
    create_instance = lambda row: db_model(**row)
    instances = []
    if isinstance(sheet_name, list):
        dfs = [
            pd.read_excel(io=file_path, header=header + offset_header, sheet_name=sheet_name_element)
            for sheet_name_element in sheet_name
        ]
        df = pd.concat(dfs, ignore_index=True)
    elif isinstance(sheet_name, str):
        df = pd.read_excel(io=file_path, header=header + offset_header, sheet_name=sheet_name)
    elif sheet_name is None:
        df = pd.read_excel(io=file_path, header=header + offset_header)
    print(f"UPDATE MODEL: Got instance from file: {len(df)} rows")
    if df_header_maper is not None:
        df = df.rename(columns=df_header_maper)
        print(f"UPDATE MODEL: Instance headers renamed")

    df.columns = df.columns.str.lower()
    print(f"UPDATE MODEL: Instance headers now in lowercase ")

    if "name" in list(df.columns):
        df = df.dropna(subset=["name"])
        print(f"UPDATE MODEL: Droped NaN in name")
    if df_date_field is not None:
        for date_field in df_date_field:
            df[date_field] = df[date_field].apply(lambda t: datetime.strptime(t, "%d.%m.%Y").date())
            print(f"UPDATE MODEL: Date was updated")

    if presave is not None:
        df = presave(df)
        print(f"UPDATE MODEL: Presave was finished")

    records = df.where(pd.notnull(df), None).to_dict("records")
    print(f"UPDATE MODEL: Instanses was conveted in dict")
    ids: list = [row.get("id") for row in records]

    statement = select(db_model).where(col(db_model.id).in_(ids))
    resutls = session.exec(statement)
    exist_instances = resutls.all()
    if len(exist_instances) == 0:
        instances = list(map(create_instance, records))
    else:
        exist_instances_ids = [row.id for row in exist_instances]
        instances += list(map(create_instance, filter(lambda row: row.get("id") not in exist_instances_ids, records)))
        for exist_instance in exist_instances:
            record = list(filter(lambda row: row.get("id") == exist_instance.id, records))[0]
            if exist_instance.dict() != record:
                for key in list(record.keys()):
                    if (value := record.get(key)) is not None:
                        setattr(exist_instance, key, value)
                instances.append(exist_instance)
    try:
        for chunk_instance in list_chunk(instances):
            session.bulk_save_objects(chunk_instance)
            session.commit()
            print(f"UPDATE MODEL: Instanses was saved in db: {len(chunk_instance)} rows")

    except Exception as err:
        print(f"ERROR: {str(err)}")
        raise
    return len(instances)


def _update_building(file_path: str):
    count_rows = 0
    count_rows += _update_model(db_model=CategoryMKD, file_path=file_path)
    count_rows += _update_model(db_model=StatusMKD, file_path=file_path)
    count_rows += _update_model(db_model=StatusManageMKD, file_path=file_path)
    count_rows += _update_model(db_model=TypeBuildingFund, file_path=file_path)
    count_rows += _update_model(db_model=TypeSocialObject, file_path=file_path)
    count_rows += _update_model(db_model=QueueClean, file_path=file_path)
    count_rows += _update_model(db_model=AttributeCrash, file_path=file_path)
    count_rows += _update_model(db_model=WallMaterial, file_path=file_path)
    count_rows += _update_model(db_model=RoofMaterial, file_path=file_path)
    count_rows += _update_model(db_model=ProjectSeries, file_path=file_path)
    count_rows += _update_model(
        db_model=Building, file_path=file_path, df_header_maper=building_df_header_mapper, presave=_presave_building
    )
    return count_rows


def _update_incident(file_path: str):
    print(f"UPDATE INCIDENT: Started")
    return _update_model(
        db_model=Incident, file_path=file_path, df_header_maper=incident_df_header_mapper, presave=_presave_incident
    )


def _update_work(file_path: str):
    return _update_model(
        db_model=Work,
        file_path=file_path,
        df_header_maper=work_df_header_mapper,
        presave=_presave_work,
        df_date_field=work_date_field,
    )


def _update_event(file_path: str):
    return _update_model(
        db_model=Event, file_path=file_path, df_header_maper=event_df_header_mapper, presave=_presave_event
    )


def _update_worktype(file_path: str):
    return _update_model(
        db_model=WorkType, file_path=file_path, df_header_maper=work_type_df_header_mapper, presave=_presave_worktype
    )


def _update_worktype_kr(file_path: str):
    return _update_model(
        db_model=WorkType,
        file_path=file_path,
        df_header_maper=work_type_kr_df_header_mapper,
        presave=_presave_worktype_kr,
        offset_header=1,
    )


def update_from_file(id: int, task) -> int:
    session = get_session().__next__()
    statement = select(FileData).where(FileData.id == id)
    resutls = session.exec(statement)
    instance = resutls.one_or_none()
    instance.task_id = task.request.id
    session.add(instance)
    session.commit()
    count_rows = 0
    try:
        match instance.file_type:
            case FileType.BUILDING.value:
                count_rows = _update_building(file_path=instance.file_path)
            case FileType.INCIDENT.value:
                count_rows = _update_incident(file_path=instance.file_path)
            case FileType.WORK.value:
                count_rows = _update_work(file_path=instance.file_path)
            case FileType.EVENT.value:
                count_rows = _update_event(file_path=instance.file_path)
            case FileType.WORK_TYPE.value:
                count_rows = _update_worktype(file_path=instance.file_path)
            case FileType.WORK_TYPE_KR.value:
                count_rows = _update_worktype_kr(file_path=instance.file_path)
    except Exception as err:
        raise Exception(f"Error {task.request.id}")
    return count_rows


def predict_works_and_incidents(
    id: int, task, street: str, source_id: int, type_fund_id: str, date_start: str, date_end: str
):
    print("START PREDICT")
    print(f"{id=}")
    print(f"{street=}")
    print(f"{source_id=}")
    print(f"{type_fund_id=}")
    print(f"{date_start=}")
    print(f"{date_end=}")
    session = get_session().__next__()
    statement = select(Plan).where(Plan.id == id)
    resutls = session.exec(statement)
    plan = resutls.one_or_none()
    print(f"Plan ID {plan.id}")

    statement = (
        select(Building)
        .where(Building.type_building_fund_id == type_fund_id)
        .where(col(Building.name).contains(street))
    )
    result = session.execute(statement)
    buildings = result.scalars().all()
    print(f"Buildings find: {len(buildings)}")

    statement = select(SourceSystem).where(SourceSystem.id == source_id)
    result = session.execute(statement)
    source_system = result.scalar_one()
    print(f"Source system: {source_system.name}")

    for building in buildings:
        works = get_works(unom=building.id, sourcesytem=source_system.name)
        if works is not None:
            print(f"Works find for building={building.id}: {len(works)}")
            for work in works.keys():
                statement = select(WorkType).where(WorkType.name == work.capitalize())
                result = session.execute(statement)
                worktype = result.scalar_one_or_none()
                if worktype is None:
                    continue
                plan_work = PlanWork(
                    acc=works.get(work).get("acc"),
                    start_day=works.get(work).get("start_day"),
                    end_day=works.get(work).get("end_day"),
                    building_id=building.id,
                    plan_id=plan.id,
                    work_id=worktype.id,
                )
                session.add(plan_work)
                session.commit()
                session.refresh(plan_work)

        incidents = get_incident(unom=building.id, sourcesytem=source_system.name)
        if incidents is not None:
            print(f"incidents find for building={building.id}: {len(incidents)}")
            for incident in incidents.keys():
                statement = select(Event).where(Event.name == incident.capitalize()).where(Event.source_id == source_id)
                result = session.execute(statement)
                incident_instance = result.scalar_one_or_none()
                if incident_instance is None:
                    continue
                plan_event = PlanEvent(
                    acc=incidents.get(incident),
                    building_id=building.id,
                    plan_id=plan.id,
                    event_id=incident_instance.id,
                )
                session.add(plan_event)
                session.commit()
                session.refresh(plan_event)
