from fastapi import APIRouter

router=APIRouter()

@router.get("/auth")
def authentication():
    return "use: authentication"