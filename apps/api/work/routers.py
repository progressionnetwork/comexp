from share.routers import CRUDRouter
from work.models import Work, WorkBase, WorkRead, WorkType, WorkTypeBase

router = CRUDRouter(create_model=WorkBase, read_model=WorkRead, update_model=WorkBase, db_model=Work)

router_worktype = CRUDRouter(
    create_model=WorkTypeBase, read_model=WorkType, update_model=WorkTypeBase, db_model=WorkType
)
