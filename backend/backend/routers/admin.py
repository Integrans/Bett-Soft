from fastapi import APIRouter

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@router.get("/")
def admin_home():
    return {"message": "Panel administrador funcionando"}
