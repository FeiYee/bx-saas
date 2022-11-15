from fastapi import APIRouter

router = APIRouter()


@router.post("/graph/node", tags=["home"])
async def node():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.post("/graph/update", tags=["home"])
async def update():
    return {"username": "fakecurrentuser"}


@router.get("/download", tags=["home"])
async def download():
    return {"username": "fakecurrentuser"}
