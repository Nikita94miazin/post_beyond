from fastapi_versioning import version

from app.custom_api_router import CustomApiRouter


router = CustomApiRouter(
    prefix="/groups",
    tags=["Group"]
)


@router.get("/ping")
@version(0, 1)
def ping():
    return {"message": "pong"}
