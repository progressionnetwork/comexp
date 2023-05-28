import uvicorn
from auth.routers import router as auth_router
from building.routers import (
    router_attribute_crash,
    router_building,
    router_category_mkd,
    router_project_series,
    router_queue_clean,
    router_roof_material,
    router_status_manage_mkd,
    router_status_mkd,
    router_type_building,
    router_type_social,
    router_wall_material,
)
from event.routers import router_event, router_sourcesystem
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from files.routers import router as files_router
from incident.routers import router as incident_router
from share.database import init_db
from starlette.requests import Request
from user.routers import router as user_router
from work.routers import router as work_router
from work.routers import router_worktype

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, err) -> JSONResponse:
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=500, content={"message": f"{base_error_message}. Detail: {err}"})


@app.on_event("startup")
async def startup_event():
    await init_db()


@app.get("/healthcheck", tags=["Healthcheck"])
async def healthcheck():
    return JSONResponse(status_code=200, content={"healthchek": True})


app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(router_building, prefix="/building", tags=["Дома"])
app.include_router(router_wall_material, prefix="/wall_material", tags=["Материал стен"])
app.include_router(router_attribute_crash, prefix="/attribute_crash", tags=["Признак аварийности здания"])
app.include_router(router_category_mkd, prefix="/category_mkd", tags=["Категория МКД"])
app.include_router(router_project_series, prefix="/project_series", tags=["Серии проектов"])
app.include_router(router_queue_clean, prefix="/queue_clean", tags=["Очередность уборки кровли"])
app.include_router(router_status_manage_mkd, prefix="/status_manage_mkd", tags=["Статусы управления МКД"])
app.include_router(router_status_mkd, prefix="/status_mkd", tags=["Статусы МКД"])
app.include_router(router_type_building, prefix="/type_building", tags=["Типы жилищного фонда"])
app.include_router(router_type_social, prefix="/type_social", tags=["Виды социальных объектов"])
app.include_router(router_roof_material, prefix="/roof_material", tags=["Материалы кровли"])
app.include_router(incident_router, prefix="/incident", tags=["Инциденты"])
app.include_router(work_router, prefix="/work", tags=["Работы"])
app.include_router(router_worktype, prefix="/worktype", tags=["Работы"])
app.include_router(router_event, prefix="/event", tags=["События"])
app.include_router(router_sourcesystem, prefix="/sourcesystem", tags=["Источники событий"])
app.include_router(files_router, prefix="/files", tags=["Файлы для обновления"])

if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)
