from incident.models import Incident, IncidentBase, IncidentRead
from share.routers import CRUDRouter

router = CRUDRouter(create_model=IncidentBase, read_model=IncidentRead, update_model=IncidentBase, db_model=Incident)
