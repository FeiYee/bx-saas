from fastapi import APIRouter

router = APIRouter()


@router.post("/stats/node", tags=["stats"])
async def node():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.post("/stats/update", tags=["stats"])
async def update():
    return {"username": "fakecurrentuser"}


@router.get("/stats/article", tags=["stats"])
async def download():
    return {"username": "fakecurrentuser"}


@router.get("/stats/download", tags=["stats"])
async def download():
    return {"username": "fakecurrentuser"}
