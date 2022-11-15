from fastapi import APIRouter

from app.home.controller import home_controller

from app.system.controller import user_controller
from app.system.controller import org_controller

from app.search.controller import search_controller
from app.search.controller import keyword_controller


from app.stats.controller import stats_controller
from app.datum.controller import datum_controller
from app.graph.controller import graph_controller

router = APIRouter()

router.include_router(home_controller.router)

router.include_router(user_controller.router)
router.include_router(org_controller.router)

router.include_router(search_controller.router)
router.include_router(keyword_controller.router)

router.include_router(stats_controller.router)
router.include_router(datum_controller.router)
router.include_router(graph_controller.router)

