from fastapi import APIRouter


router = APIRouter(
    prefix="/books",
    tags=["books"],
)


@router.get("/")
async def read_books():
    return {"books": "read books"}


@router.post("/")
async def post_books():
    return {"books": "post book"}
