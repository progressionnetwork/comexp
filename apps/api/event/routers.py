from event.models import Event, EventBase, EventRead, SourceSystem, SourceSystemBase, SourceSystemRead
from share.routers import CRUDRouter

router_sourcesystem = CRUDRouter(
    create_model=SourceSystemBase, update_model=SourceSystemBase, read_model=SourceSystemRead, db_model=SourceSystem
)

router_event = CRUDRouter(create_model=EventBase, update_model=EventBase, read_model=EventRead, db_model=Event)
