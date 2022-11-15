from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def home():
    return {"message": "Home"}


@router.post("/login", tags=["home"])
async def login():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.post("/logout", tags=["home"])
async def logout():
    return {"username": "fakecurrentuser"}


@router.get("/users", tags=["home"])
async def user():
    return {"username": "fakecurrentuser"}
