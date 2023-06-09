from event.models import Event, EventBase, EventRead, SourceSystem, SourceSystemBase, SourceSystemRead
from share.routers import CRUDRouter
from worker.tasks import update_incident_priority

router_sourcesystem = CRUDRouter(
    create_model=SourceSystemBase, update_model=SourceSystemBase, read_model=SourceSystemRead, db_model=SourceSystem
)

router_event = CRUDRouter(create_model=EventBase, update_model=EventBase, read_model=EventRead, db_model=Event)


@router_event.get("/update_priority/")
async def update_event_priority(
    # current_user=Depends(get_current_user_with_permmissions(model="OKPD2", type_permissions="read")),
):
    update_incident_priority.delay()
    return {"result": True}
