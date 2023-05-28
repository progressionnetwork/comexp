from auth.dependencies import get_current_user_with_permmissions
from fastapi import APIRouter, Depends
from share.database import get_session
from share.services import count as count_instance
from share.services import create as create_instance
from share.services import delete_all as delete_all_instances
from share.services import delete_one as delete_instance
from share.services import get_all as get_all_instances
from share.services import get_one as get_instance
from share.services import update as update_instance
from share.types import BoolResponse
from share.utils import pagination
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel


class CRUDRouter(APIRouter):
    create_model: SQLModel
    read_model: SQLModel
    update_model: SQLModel
    db_model: SQLModel

    def __init__(
        self,
        create_model: SQLModel,
        read_model: SQLModel,
        update_model: SQLModel,
        db_model: SQLModel,
        create: bool = True,
        get_all: bool = True,
        get_one: bool = True,
        get_count: bool = True,
        update: bool = True,
        delete_one: bool = True,
        delete_all: bool = True,
        *args,
        **kwargs,
    ) -> None:
        self.create_model = create_model
        self.read_model = read_model
        self.update_model = update_model
        self.db_model = db_model
        super().__init__(*args, **kwargs)

        if create:
            self.add_api_route(
                path="/",
                endpoint=self.db_create(),
                response_model=self.read_model,
                summary="Create one record",
                methods=["POST"],
            )

        if get_all:
            self.add_api_route(
                path="/",
                endpoint=self.db_get_all(),
                response_model=list[self.read_model],
                summary="Get all record",
                methods=["GET"],
                # response_model_exclude_none=True,
            )

        if get_one:
            self.add_api_route(
                path="/{id}",
                endpoint=self.db_get_one(),
                response_model=self.read_model,
                summary="Get one record",
                methods=["GET"],
                # response_model_exclude_none=True
            )

        if get_count:
            self.add_api_route(
                path="/count/",
                endpoint=self.db_count(),
                summary="Get counts",
                response_model=int,
                methods=["GET"],
                # response_model_exclude_none=True
            )

        if update:
            self.add_api_route(
                path="/{id}",
                endpoint=self.db_update(),
                response_model=self.read_model,
                summary="Update one record",
                methods=["PATCH"],
            )

        if delete_one:
            self.add_api_route(
                path="/{id}",
                endpoint=self.db_delete_one(),
                response_model=BoolResponse,
                summary="Delete one record",
                methods=["DELETE"],
            )

        if delete_all:
            self.add_api_route(
                path="/",
                endpoint=self.db_delete_all(),
                response_model=BoolResponse,
                summary="Delete all record",
                methods=["DELETE"],
            )

    def api_route(self, path: str, *args: any, **kwargs: any):
        methods = kwargs.get("methods", ["GET"])
        self.remove_api_route(path, methods)
        return super().api_route(path, *args, **kwargs)

    def get(self, path: str, *args: any, **kwargs: any):
        self.remove_api_route(path, ["GET"])
        return super().get(path, *args, **kwargs)

    def post(self, path: str, *args: any, **kwargs: any):
        self.remove_api_route(path, ["POST"])
        return super().post(path, *args, **kwargs)

    def put(self, path: str, *args: any, **kwargs: any):
        self.remove_api_route(path, ["PUT"])
        return super().put(path, *args, **kwargs)

    def delete(self, path: str, *args: any, **kwargs: any):
        self.remove_api_route(path, ["DELETE"])
        return super().delete(path, *args, **kwargs)

    def remove_api_route(self, path: str, methods: list[str]) -> None:
        methods_ = set(methods)
        for route in self.routes:
            if (
                route.path == f"{path}"  # type: ignore
                and route.methods == methods_  # type: ignore
            ):
                self.routes.remove(route)

    def db_create(self, *args, **kwargs):
        async def route(
            create_model: self.create_model,
            session: AsyncSession = Depends(get_session),
            # current_user=Depends(
            #     get_current_user_with_permmissions(model=self.db_model.__name__, type_permissions="write")
            # ),
        ) -> self.read_model:
            return await create_instance(session=session, create_model=create_model, db_model=self.db_model)

        return route

    def db_get_all(self, *args, **kwargs):
        async def route(
            session: AsyncSession = Depends(get_session),
            pagination: dict = Depends(pagination),
            # current_user=Depends(
            #     get_current_user_with_permmissions(model=self.db_model.__name__, type_permissions="read")
            # ),
        ) -> list[self.read_model]:
            return await get_all_instances(
                session=session,
                offset=pagination.get("offset"),
                limit=pagination.get("limit"),
                db_model=self.db_model,
            )

        return route

    def db_get_one(self, *args, **kwargs):
        async def route(
            id: int,
            session: AsyncSession = Depends(get_session),
            # current_user=Depends(
            #     get_current_user_with_permmissions(model=self.db_model.__name__, type_permissions="read")
            # ),
        ) -> self.read_model:
            return await get_instance(session=session, id=id, db_model=self.db_model)

        return route

    def db_count(self, *args, **kwargs):
        async def route(
            session: AsyncSession = Depends(get_session),
            # current_user=Depends(
            #     get_current_user_with_permmissions(model=self.db_model.__name__, type_permissions="read")
            # ),
        ) -> self.read_model:
            return await count_instance(session=session, db_model=self.db_model)

        return route

    def db_update(self, *args, **kwargs):
        async def route(
            id: int,
            update_model: self.update_model,
            session: AsyncSession = Depends(get_session),
            # current_user=Depends(
            #     get_current_user_with_permmissions(model=self.db_model.__name__, type_permissions="write")
            # ),
        ) -> SQLModel:
            return await update_instance(session=session, id=id, update_model=update_model, db_model=self.db_model)

        return route

    def db_delete_one(self, *args, **kwargs):
        async def route(
            id: int,
            session: AsyncSession = Depends(get_session),
            # current_user=Depends(
            #     get_current_user_with_permmissions(model=self.db_model.__name__, type_permissions="delete")
            # ),
        ) -> BoolResponse:
            return await delete_instance(session=session, id=id, db_model=self.db_model)

        return route

    def db_delete_all(self, *args, **kwargs):
        async def route(
            session: AsyncSession = Depends(get_session),
            # current_user=Depends(
            #     get_current_user_with_permmissions(model=self.db_model.__name__, type_permissions="delete")
            # ),
        ) -> BoolResponse:
            return await delete_all_instances(session=session, db_model=self.db_model)

        return route
